#!/bin/bash
# Recovery script — run after VM is rebooted
# Fixes and re-runs the 5 failed pipelines
set -euo pipefail

VM_HOST="aliduabubakari@roberto-vm.vpn.sintef"
VM_BASE="/home/aliduabubakari/custom_pipelines"
LOCAL_BASE="/Users/abubakarialidu/Downloads/custom_pipelines"

echo "=== 1. Deep clean VM ==="
ssh "$VM_HOST" "
sudo docker system prune -af --volumes 2>/dev/null || true
sudo k3s ctr images ls -q 2>/dev/null | xargs -I{} sudo k3s ctr images rm {} 2>/dev/null || true
kubectl delete pvc --all -n default --force --grace-period=0 2>/dev/null || true
sudo rm -rf /tmp/*.tar
echo 'Clean OK'
"

echo "=== 2. Sync fixed pipelines ==="
for pipe in 003_credit_risk 004_customer_churn 025_sports_regression_prediction_statistical_v2 060_transportation_cleaning_integration_validation 090_transportation_statistical_visualization_integration_v2; do
    rsync -az --exclude='output/' --exclude='*.parquet' --exclude='*.pkl' \
        "${LOCAL_BASE}/${pipe}/" "${VM_HOST}:${VM_BASE}/${pipe}/"
done
scp "${LOCAL_BASE}/_argo_live_test/argo_batch_runner.sh" "${VM_HOST}:${VM_BASE}/argo_batch_runner.sh"

echo "=== 3. Re-run 5 failures ==="
ssh "$VM_HOST" "cd ${VM_BASE} && bash argo_batch_runner.sh ${VM_BASE}/argo_live_results 99 \
    ${VM_BASE}/003_credit_risk \
    ${VM_BASE}/004_customer_churn \
    ${VM_BASE}/025_sports_regression_prediction_statistical_v2 \
    ${VM_BASE}/060_transportation_cleaning_integration_validation \
    ${VM_BASE}/090_transportation_statistical_visualization_integration_v2"

echo "=== 4. Pull results ==="
rsync -az --exclude='*.tar' "${VM_HOST}:${VM_BASE}/argo_live_results/" "${LOCAL_BASE}/argo_live_results/"

echo "=== 5. Generate final summary ==="
python3 "${LOCAL_BASE}/_argo_live_test/generate_summary.py"

echo ""
echo "Done! Check ${LOCAL_BASE}/argo_live_results/SUMMARY.txt"
