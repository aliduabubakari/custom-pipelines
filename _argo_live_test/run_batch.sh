#!/bin/bash
# Argo Live Batch Runner - Runs on the VM
# Usage: ./run_batch.sh <batch_num> <pipeline_dir_1> <pipeline_dir_2> ...

set -euo pipefail

BATCH_NUM="$1"
shift
PIPELINES=("$@")
BASE_DIR="/home/aliduabubakari/custom_pipelines"
RESULTS_DIR="${BASE_DIR}/argo_live_results/batch_${BATCH_NUM}"
LOG_FILE="${RESULTS_DIR}/batch.log"

mkdir -p "$RESULTS_DIR"

log() { echo "[$(date '+%H:%M:%S')] $*" | tee -a "$LOG_FILE"; }

###############################################################################
# 1. BUILD & IMPORT IMAGES
###############################################################################
log "=== BATCH $BATCH_NUM: Building ${#PIPELINES[@]} images ==="

declare -A IMAGE_TAGS

for pipe_dir in "${PIPELINES[@]}"; do
    pipeline_name=$(basename "$pipe_dir")
    image_tag="pipeline-${pipeline_name}:latest"
    IMAGE_TAGS["$pipeline_name"]="$image_tag"

    log "  Building: $image_tag"
    sudo docker build -t "$image_tag" "$pipe_dir" >> "$LOG_FILE" 2>&1
    build_ok=$?

    if [ $build_ok -ne 0 ]; then
        log "  ✗ BUILD FAILED: $pipeline_name (exit=$build_ok)"
        echo "{\"status\":\"BUILD_FAILED\",\"exit_code\":$build_ok}" > "${RESULTS_DIR}/${pipeline_name}_result.json"
        continue
    fi

    # Save and import into K3s containerd
    tar_path="/tmp/${pipeline_name}.tar"
    sudo docker save "$image_tag" -o "$tar_path" 2>> "$LOG_FILE"
    sudo k3s ctr images import "$tar_path" >> "$LOG_FILE" 2>&1
    rm -f "$tar_path"
    log "  ✓ Built & imported: $image_tag"
done

log "=== BATCH $BATCH_NUM: Submitting workflows ==="

###############################################################################
# 2. SUBMIT WORKFLOWS
###############################################################################
declare -A WF_NAMES

for pipe_dir in "${PIPELINES[@]}"; do
    pipeline_name=$(basename "$pipe_dir")
    image_tag="${IMAGE_TAGS[$pipeline_name]:-}"

    if [ -z "$image_tag" ]; then
        continue  # build failed
    fi

    # Modify YAML to use our image and add artifact collection
    yaml_path="${pipe_dir}/pipeline.yaml"

    # Submit via argo
    wf_name=$(argo submit "$yaml_path" \
        --name "${pipeline_name}" \
        --parameter image="$image_tag" \
        -o json 2>> "$LOG_FILE" | python3 -c "import sys,json; print(json.load(sys.stdin)['metadata']['name'])" 2>> "$LOG_FILE")

    WF_NAMES["$pipeline_name"]="$wf_name"
    log "  Submitted: $pipeline_name → $wf_name"
done

###############################################################################
# 3. WAIT & COLLECT METRICS
###############################################################################
log "=== BATCH $BATCH_NUM: Waiting for completion ==="

TIMEOUT=600  # 10 min per pipeline max
POLL_INTERVAL=5

for pipe_dir in "${PIPELINES[@]}"; do
    pipeline_name=$(basename "$pipe_dir")
    wf_name="${WF_NAMES[$pipeline_name]:-}"

    if [ -z "$wf_name" ]; then
        continue
    fi

    log "  Waiting: $pipeline_name ($wf_name)"

    # Poll for completion
    elapsed=0
    while [ $elapsed -lt $TIMEOUT ]; do
        status=$(argo get "$wf_name" -o json 2>/dev/null | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(d.get('status',{}).get('phase','Running'))
" 2>/dev/null || echo "Running")

        if [ "$status" = "Succeeded" ] || [ "$status" = "Failed" ] || [ "$status" = "Error" ]; then
            break
        fi
        sleep $POLL_INTERVAL
        elapsed=$((elapsed + POLL_INTERVAL))
    done

    if [ $elapsed -ge $TIMEOUT ]; then
        status="Timeout"
    fi

    log "  Result: $pipeline_name → $status (${elapsed}s)"

    # Collect full workflow JSON
    argo get "$wf_name" -o json > "${RESULTS_DIR}/${pipeline_name}_workflow.json" 2>> "$LOG_FILE"

    # Collect logs
    argo logs "$wf_name" --no-color > "${RESULTS_DIR}/${pipeline_name}_logs.txt" 2>> "$LOG_FILE"

    # Collect resource metrics per pod
    kubectl get pods -l "workflows.argoproj.io/workflow=${wf_name}" -o name 2>/dev/null | while read pod; do
        pod_name=$(basename "$pod")
        kubectl top pod "$pod_name" --no-headers 2>/dev/null >> "${RESULTS_DIR}/${pipeline_name}_resources.txt" || true
    done

    # Generate per-pipeline result JSON
    node_count=$(python3 -c "
import json
with open('${RESULTS_DIR}/${pipeline_name}_workflow.json') as f:
    d = json.load(f)
nodes = d.get('status',{}).get('nodes',{})
print(len([n for n in nodes.values() if n.get('type')=='Pod']))
" 2>/dev/null || echo "0")

    duration=$(python3 -c "
import json
with open('${RESULTS_DIR}/${pipeline_name}_workflow.json') as f:
    d = json.load(f)
print(d.get('status',{}).get('finishedAt',''))
" 2>/dev/null || echo "")

    # Check for step-level failures
    failed_steps=$(python3 -c "
import json
with open('${RESULTS_DIR}/${pipeline_name}_workflow.json') as f:
    d = json.load(f)
nodes = d.get('status',{}).get('nodes',{})
failed = []
for nid, n in nodes.items():
    if n.get('type') == 'Pod' and n.get('phase') in ('Failed','Error'):
        failed.append({
            'step': n.get('displayName', nid),
            'phase': n.get('phase'),
            'message': n.get('message',''),
            'exitCode': n.get('outputs',{}).get('exitCode','')
        })
print(json.dumps(failed))
" 2>/dev/null || echo "[]")

    cat > "${RESULTS_DIR}/${pipeline_name}_result.json" << EOF
{
  "pipeline": "$pipeline_name",
  "batch": $BATCH_NUM,
  "workflow_name": "$wf_name",
  "status": "$status",
  "duration_seconds": $elapsed,
  "node_count": $node_count,
  "finished_at": "$duration",
  "failed_steps": $failed_steps,
  "image_tag": "${IMAGE_TAGS[$pipeline_name]}"
}
EOF

done

###############################################################################
# 4. CLEANUP
###############################################################################
log "=== BATCH $BATCH_NUM: Cleanup ==="

for pipe_dir in "${PIPELINES[@]}"; do
    pipeline_name=$(basename "$pipe_dir")
    wf_name="${WF_NAMES[$pipeline_name]:-}"
    image_tag="${IMAGE_TAGS[$pipeline_name]:-}"

    # Delete workflow
    [ -n "$wf_name" ] && argo delete "$wf_name" 2>> "$LOG_FILE" || true

    # Remove image from containerd
    [ -n "$image_tag" ] && sudo k3s ctr images rm "docker.io/library/${image_tag}" 2>> "$LOG_FILE" || true

    # Remove docker image
    [ -n "$image_tag" ] && sudo docker rmi "$image_tag" 2>> "$LOG_FILE" || true
done

# Prune dangling
sudo docker image prune -f >> "$LOG_FILE" 2>&1 || true

log "=== BATCH $BATCH_NUM: DONE ==="
