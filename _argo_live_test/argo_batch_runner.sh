#!/bin/bash
# Argo Live Batch Runner — VM-side
# Usage: ./argo_batch_runner.sh <results_dir> <batch_num> <pipe_dir_1> [pipe_dir_2 ...]
# Saves per-pipeline results to: <results_dir>/<pipeline_name>/
set -euo pipefail

RESULTS_DIR="$1"
BATCH_NUM="$2"
shift 2
PIPELINES=("$@")
LOG_FILE="${RESULTS_DIR}/batch_${BATCH_NUM}.log"
METRICS_FILE="${RESULTS_DIR}/batch_${BATCH_NUM}_metrics.jsonl"

mkdir -p "$RESULTS_DIR"

log() { echo "[$(date '+%H:%M:%S')] B${BATCH_NUM}: $*" | tee -a "$LOG_FILE"; }

###############################################################################
# PHASE 1: BUILD & IMPORT
###############################################################################
log "Building ${#PIPELINES[@]} images..."

declare -A BUILD_STATUS IMAGE_TAGS

for pipe_dir in "${PIPELINES[@]}"; do
    pipeline_name=$(basename "$pipe_dir")

    # Extract image name from YAML
    image_tag=$(python3 -c "
import yaml, sys
with open('${pipe_dir}/pipeline.yaml') as f:
    for doc in yaml.safe_load_all(f):
        if doc and 'spec' in doc:
            for t in doc['spec'].get('templates', []):
                if 'container' in t:
                    print(t['container'].get('image', ''))
                    sys.exit(0)
print('')
" 2>/dev/null)

    if [ -z "$image_tag" ]; then
        log "  ✗ $pipeline_name: no image in YAML"
        BUILD_STATUS["$pipeline_name"]="NO_IMAGE"
        continue
    fi

    IMAGE_TAGS["$pipeline_name"]="$image_tag"

    # Build
    log "  Building $image_tag..."
    if sudo docker build -t "$image_tag" "$pipe_dir" >> "$LOG_FILE" 2>&1; then
        # Save + import to K3s
        tar_path="/tmp/${pipeline_name}.tar"
        sudo docker save "$image_tag" -o "$tar_path" 2>> "$LOG_FILE"
        sudo k3s ctr images import "$tar_path" >> "$LOG_FILE" 2>&1
        sudo rm -f "$tar_path"
        log "  ✓ $pipeline_name built & imported"
        BUILD_STATUS["$pipeline_name"]="OK"
    else
        log "  ✗ $pipeline_name: BUILD FAILED"
        BUILD_STATUS["$pipeline_name"]="BUILD_FAIL"
    fi
done

###############################################################################
# PHASE 2: SUBMIT WORKFLOWS
###############################################################################
log "Submitting workflows..."

declare -A WF_NAMES

for pipe_dir in "${PIPELINES[@]}"; do
    pipeline_name=$(basename "$pipe_dir")
    [ "${BUILD_STATUS[$pipeline_name]:-}" != "OK" ] && continue

    yaml_path="${pipe_dir}/pipeline.yaml"
    # Sanitize workflow name: underscores→hyphens, lowercase, alphanumeric+hyphens only
    safe_name=$(echo "${pipeline_name}" | tr '_' '-' | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9-]//g' | sed 's/--*/-/g' | sed 's/^-//' | sed 's/-$//')
    prefix="p-${BATCH_NUM}-"
    max_safe_len=$((63 - ${#prefix}))
    safe_name=$(echo "$safe_name" | cut -c1-$max_safe_len | sed 's/-$//')
    wf_name="${prefix}${safe_name}"

    if argo submit "$yaml_path" --name "$wf_name" >> "$LOG_FILE" 2>&1; then
        WF_NAMES["$pipeline_name"]="$wf_name"
        log "  Submitted: $pipeline_name → $wf_name"
    else
        log "  ✗ $pipeline_name: SUBMIT FAILED"
        BUILD_STATUS["$pipeline_name"]="SUBMIT_FAIL"
    fi
done

###############################################################################
# PHASE 3: WAIT & COLLECT
###############################################################################
log "Waiting for completion (timeout=600s)..."

TIMEOUT=600
POLL=5

for pipe_dir in "${PIPELINES[@]}"; do
    pipeline_name=$(basename "$pipe_dir")
    wf_name="${WF_NAMES[$pipeline_name]:-}"
    [ -z "$wf_name" ] && continue

    # Create per-pipeline result folder
    PIPE_RESULTS="${RESULTS_DIR}/${pipeline_name}"
    mkdir -p "$PIPE_RESULTS"

    elapsed=0
    phase="Running"
    while [ $elapsed -lt $TIMEOUT ]; do
        phase=$(argo get "$wf_name" -o json 2>/dev/null | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(d.get('status',{}).get('phase','Running'))
" 2>/dev/null || echo "Running")
        [ "$phase" = "Succeeded" ] || [ "$phase" = "Failed" ] || [ "$phase" = "Error" ] && break
        sleep $POLL
        elapsed=$((elapsed + POLL))
    done
    [ $elapsed -ge $TIMEOUT ] && phase="Timeout"

    log "  $pipeline_name: $phase (${elapsed}s)"

    # Save workflow JSON
    argo get "$wf_name" -o json > "${PIPE_RESULTS}/workflow.json" 2>> "$LOG_FILE" || true

    # Save logs
    argo logs "$wf_name" --no-color > "${PIPE_RESULTS}/logs.txt" 2>> "$LOG_FILE" || true

    # Extract structured metrics
    python3 -c "
import json, sys
from datetime import datetime

try:
    with open('${PIPE_RESULTS}/workflow.json') as f:
        d = json.load(f)
    nodes = d.get('status',{}).get('nodes',{})
    steps = []
    total_duration = 0
    for nid, n in sorted(nodes.items()):
        if n.get('type') == 'Pod':
            started = n.get('startedAt','')
            finished = n.get('finishedAt','')
            step_dur = 0
            if started and finished:
                try:
                    s = datetime.fromisoformat(started.replace('Z','+00:00'))
                    f = datetime.fromisoformat(finished.replace('Z','+00:00'))
                    step_dur = round((f-s).total_seconds(), 1)
                except: pass
            steps.append({
                'name': n.get('displayName', nid),
                'phase': n.get('phase','?'),
                'duration_s': step_dur,
                'exit_code': n.get('outputs',{}).get('exitCode',''),
                'message': str(n.get('message',''))[:300]
            })
            total_duration += step_dur

    resources = d.get('status',{}).get('resourcesDuration',{})
    
    result = {
        'pipeline': '${pipeline_name}',
        'batch': ${BATCH_NUM},
        'workflow': '${wf_name}',
        'phase': '${phase}',
        'elapsed_s': ${elapsed},
        'pod_duration_s': round(total_duration, 1),
        'node_count': sum(1 for n in nodes.values() if n.get('type')=='Pod'),
        'step_count': len(steps),
        'steps_succeeded': sum(1 for s in steps if s['phase']=='Succeeded'),
        'steps_failed': sum(1 for s in steps if s['phase'] in ('Failed','Error')),
        'steps': steps,
        'image_tag': '${IMAGE_TAGS[$pipeline_name]:-}',
        'started_at': d.get('status',{}).get('startedAt',''),
        'finished_at': d.get('status',{}).get('finishedAt',''),
        'cpu_seconds': resources.get('cpu', 0) if isinstance(resources, dict) else 0,
        'memory_mb_seconds': resources.get('memory', 0) if isinstance(resources, dict) else 0,
    }
    with open('${PIPE_RESULTS}/metrics.json', 'w') as f:
        json.dump(result, f, indent=2)
    print(json.dumps(result))
except Exception as e:
    err = {'pipeline':'${pipeline_name}','phase':'${phase}','error':str(e)}
    with open('${PIPE_RESULTS}/metrics.json', 'w') as f:
        json.dump(err, f, indent=2)
    print(json.dumps(err))
" >> "$METRICS_FILE" 2>/dev/null || echo "{\"pipeline\":\"${pipeline_name}\",\"phase\":\"${phase}\",\"error\":\"metrics_failed\"}" >> "$METRICS_FILE"

done

###############################################################################
# PHASE 4: CLEANUP
###############################################################################
log "Cleaning up..."

for pipe_dir in "${PIPELINES[@]}"; do
    pipeline_name=$(basename "$pipe_dir")
    wf_name="${WF_NAMES[$pipeline_name]:-}"

    # Delete workflow
    [ -n "$wf_name" ] && argo delete "$wf_name" 2>> "$LOG_FILE" || true

    # Remove image from K3s containerd
    image_tag="${IMAGE_TAGS[$pipeline_name]:-}"
    [ -n "$image_tag" ] && sudo k3s ctr images rm "docker.io/${image_tag}" 2>> "$LOG_FILE" || true

    # Remove from docker
    [ -n "$image_tag" ] && sudo docker rmi "$image_tag" 2>> "$LOG_FILE" || true
done

# Prune docker
sudo docker image prune -af >> "$LOG_FILE" 2>&1 || true
sudo docker builder prune -af >> "$LOG_FILE" 2>&1 || true

log "BATCH $BATCH_NUM COMPLETE"
