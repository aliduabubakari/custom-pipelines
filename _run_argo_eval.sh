#!/bin/bash
# Argo workflow evaluator - batch runner
BASE="/Users/abubakarialidu/Downloads/custom_pipelines"
EVAL_DIR="/Users/abubakarialidu/Argo_workflow_ex"
OUT_DIR="$BASE/argo_workflow_evaluations"
mkdir -p "$OUT_DIR"

# Get all pipelines sorted, skip already-evaluated ones
pipelines=()
for d in "$BASE"/*/; do
    dirname=$(basename "$d")
    [[ "$dirname" =~ ^(docs|_batch|argo_) ]] && continue
    [ -f "$OUT_DIR/${dirname}.json" ] && continue
    pipelines+=("$dirname")
done

echo "=== Starting Argo evaluation of ${#pipelines[@]} pipelines ==="
echo ""

count=0
total=${#pipelines[@]}
failed=""

for dirname in "${pipelines[@]}"; do
    yaml="$BASE/$dirname/pipeline.yaml"
    out="$OUT_DIR/${dirname}.json"
    echo "[$((count+1))/$total] $dirname ..."
    result=$(cd "$EVAL_DIR" && python3 -m argo_workflow_evaluator "$yaml" --out "$out" 2>&1)
    exit_code=$?
    if [ $exit_code -eq 0 ]; then
        # Extract scores from output
        gates=$(echo "$result" | grep "Platform gates:" | grep -oE '(True|False)')
        combined=$(echo "$result" | grep "Combined:" | grep -oE '[0-9]+\.[0-9]+')
        sat=$(echo "$result" | grep "SAT:" | grep -oE '[0-9]+\.[0-9]+')
        pct=$(echo "$result" | grep "PCT:" | grep -oE '[0-9]+\.[0-9]+')
        echo "   ✓ Gates:$gates SAT:$sat PCT:$pct Combined:$combined"
    else
        echo "   ✗ FAILED (exit=$exit_code)"
        failed="$failed $dirname"
    fi
    count=$((count+1))
    
    # Break every 10 for batching
    if [ $((count % 10)) -eq 0 ] && [ $count -lt $total ]; then
        echo ""
        echo "--- Batch of 10 complete ($count/$total) ---"
        echo ""
    fi
done

echo ""
echo "=== DONE: $count pipelines evaluated ==="
[ -n "$failed" ] && echo "FAILED: $failed" || echo "All passed!"
