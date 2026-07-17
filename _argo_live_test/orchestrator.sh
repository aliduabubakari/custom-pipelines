#!/bin/bash
# Master Orchestrator — runs on Mac, controls VM batches via tmux
# Usage: ./orchestrator.sh [batch_size=5] [start_batch=1]
set -euo pipefail

BATCH_SIZE="${1:-5}"
START_BATCH="${2:-1}"
VM_HOST="aliduabubakari@roberto-vm.vpn.sintef"
VM_BASE="/home/aliduabubakari/custom_pipelines"
LOCAL_BASE="/Users/abubakarialidu/Downloads/custom_pipelines"
RESULTS_LOCAL="${LOCAL_BASE}/argo_live_results"
RESULTS_VM="${VM_BASE}/argo_live_results"

mkdir -p "$RESULTS_LOCAL"

echo "============================================================"
echo " ARGO LIVE PIPELINE EVALUATOR"
echo " Batch size: $BATCH_SIZE | Start at batch: $START_BATCH"
echo " VM: $VM_HOST"
echo " Results: $RESULTS_LOCAL"
echo " $(date)"
echo "============================================================"

# Step 1: Sync all pipeline code to VM
echo ""
echo "=== Syncing pipeline code to VM ==="
rsync -avz --progress \
    --exclude='output/' \
    --exclude='*.parquet' \
    --exclude='*.pkl' \
    --exclude='*.pyc' \
    --exclude='__pycache__/' \
    --exclude='_batch_*' \
    --exclude='_execution_log*' \
    --exclude='argo_workflow_evaluations/' \
    --exclude='argo_live_results/' \
    --exclude='docs/' \
    --exclude='_run_*' \
    --exclude='_generate_*' \
    --exclude='_argo_live_test/' \
    --exclude='README.md' \
    --exclude='.git/' \
    "${LOCAL_BASE}/" "${VM_HOST}:${VM_BASE}/" 2>&1 | tail -3

# Step 2: Copy the batch runner
echo ""
echo "=== Copying batch runner ==="
scp "${LOCAL_BASE}/_argo_live_test/argo_batch_runner.sh" "${VM_HOST}:${VM_BASE}/argo_batch_runner.sh"
ssh "$VM_HOST" "chmod +x ${VM_BASE}/argo_batch_runner.sh"

# Step 3: Get pipeline list
PIPELINES=($(cd "${LOCAL_BASE}" && ls -d */ | grep -E '^[0-9]+_' | sed 's|/$||' | sort))
TOTAL=${#PIPELINES[@]}
echo ""
echo "Total pipelines: $TOTAL"

# Step 4: Run batches
BATCH_NUM=$START_BATCH
IDX=0

while [ $IDX -lt $TOTAL ]; do
    BATCH_PIPES=()
    for i in $(seq 0 $((BATCH_SIZE - 1))); do
        [ $((IDX + i)) -ge $TOTAL ] && break
        BATCH_PIPES+=("${PIPELINES[$((IDX + i))]}")
    done

    echo ""
    echo "============================================================"
    echo "  BATCH $BATCH_NUM (pipelines $((IDX+1))-$((IDX+${#BATCH_PIPES[@]}))/$TOTAL)"
    echo "  ${BATCH_PIPES[*]}"
    echo "============================================================"

    # Build args for VM command
    ARGS="$BATCH_NUM"
    for p in "${BATCH_PIPES[@]}"; do
        ARGS="$ARGS ${VM_BASE}/${p}"
    done

    # Run batch on VM
    ssh "$VM_HOST" "cd ${VM_BASE} && bash argo_batch_runner.sh ${VM_BASE}/argo_live_results $ARGS" 2>&1 | grep -E "^\s*\[|✓|✗|BATCH"

    echo ""
    echo "--- Batch $BATCH_NUM complete. Pulling results... ---"

    # Pull results for this batch immediately
    rsync -avz --exclude='*.tar' "${VM_HOST}:${VM_BASE}/argo_live_results/" "${RESULTS_LOCAL}/" 2>&1 | tail -3

    # Quick summary of batch
    python3 -c "
import json, os, glob
batch_dir = '${RESULTS_LOCAL}'
# Find pipelines from this batch
for p in '${BATCH_PIPES[*]}'.split():
    metrics_file = os.path.join(batch_dir, p, 'metrics.json')
    if os.path.exists(metrics_file):
        with open(metrics_file) as f:
            m = json.load(f)
        steps_ok = f\"{m.get('steps_succeeded',0)}/{m.get('step_count',0)}\"
        dur = m.get('elapsed_s', 0)
        print(f\"  {'✅' if m.get('phase')=='Succeeded' else '❌'} {p[:55]:55s} {m.get('phase','?'):10s} {dur:>4.0f}s  steps={steps_ok}\")
    else:
        metrics_file_vm = os.path.join(batch_dir, 'batch_${BATCH_NUM}_metrics.jsonl')
        print(f'  ⚠️  {p[:55]:55s} (no metrics yet)')
" 2>/dev/null || echo "  (metrics pending)"

    IDX=$((IDX + BATCH_SIZE))
    BATCH_NUM=$((BATCH_NUM + 1))
done

# Step 5: Final pull
echo ""
echo "=== Final pull of results ==="
rsync -avz --exclude='*.tar' "${VM_HOST}:${VM_BASE}/argo_live_results/" "${RESULTS_LOCAL}/" 2>&1 | tail -3

# Step 6: Generate master summary
echo ""
echo "=== Generating master summary ==="
python3 "${LOCAL_BASE}/_argo_live_test/generate_summary.py"

echo ""
echo "============================================================"
echo " EVALUATION COMPLETE"
echo " Results: $RESULTS_LOCAL"
echo "============================================================"
