#!/bin/bash
# Sync pipeline code to VM and run Argo live tests in batches
# Usage: ./sync_and_run.sh [batch_size=5]

set -euo pipefail

BATCH_SIZE="${1:-5}"
VM_HOST="aliduabubakari@roberto-vm.vpn.sintef"
VM_BASE="/home/aliduabubakari/custom_pipelines"
LOCAL_BASE="/Users/abubakarialidu/Downloads/custom_pipelines"

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
    --exclude='README.md' \
    "${LOCAL_BASE}/" "${VM_HOST}:${VM_BASE}/"

echo ""
echo "=== Copying batch runner to VM ==="
scp "${LOCAL_BASE}/_argo_live_test/run_batch.sh" "${VM_HOST}:${VM_BASE}/run_batch.sh"
ssh "$VM_HOST" "chmod +x ${VM_BASE}/run_batch.sh"

echo ""
echo "=== Getting pipeline list ==="
# Get all pipeline dirs sorted
PIPELINES=($(ls -d "${LOCAL_BASE}"/*/ | grep -E '/[0-9]+_' | sort | xargs -I{} basename {}))

echo "Found ${#PIPELINES[@]} pipelines. Running in batches of $BATCH_SIZE."

BATCH_NUM=1
COUNT=0
BATCH_PIPES=()

for pipe in "${PIPELINES[@]}"; do
    BATCH_PIPES+=("$pipe")
    COUNT=$((COUNT + 1))

    if [ $((COUNT % BATCH_SIZE)) -eq 0 ] || [ $COUNT -eq ${#PIPELINES[@]} ]; then
        echo ""
        echo "============================================================"
        echo "  BATCH $BATCH_NUM: ${BATCH_PIPES[*]}"
        echo "============================================================"

        # Build args for VM command
        ARGS="$BATCH_NUM"
        for p in "${BATCH_PIPES[@]}"; do
            ARGS="$ARGS ${VM_BASE}/${p}"
        done

        ssh "$VM_HOST" "cd ${VM_BASE} && bash run_batch.sh $ARGS" 2>&1 | tail -20

        BATCH_NUM=$((BATCH_NUM + 1))
        BATCH_PIPES=()
    fi
done

echo ""
echo "=== All batches complete ==="

# Pull results back
echo "=== Pulling results ==="
rsync -avz "${VM_HOST}:${VM_BASE}/argo_live_results/" "${LOCAL_BASE}/argo_live_results/"
