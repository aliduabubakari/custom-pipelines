#!/bin/bash
# Run all pipelines that are missing output directories
BASE="/Users/abubakarialidu/Downloads/custom_pipelines"
LOG="$BASE/_execution_log.txt"

echo "=== PIPELINE EXECUTION LOG - $(date) ===" > "$LOG"
echo "" >> "$LOG"

SUCCESS=0
FAILED=0
SKIPPED=0

for dir in "$BASE"/*/; do
    dirname=$(basename "$dir")
    # Skip non-pipeline dirs
    [[ "$dirname" =~ ^(docs|_batch) ]] && continue
    # Skip if output already exists
    if [ -d "$dir/output" ]; then
        echo "SKIP: $dirname (output exists)" | tee -a "$LOG"
        SKIPPED=$((SKIPPED+1))
        continue
    fi
    # Run pipeline
    echo "===== RUNNING: $dirname =====" | tee -a "$LOG"
    mkdir -p "$dir/output"
    ok=1
    for step in step_01_load.py step_02_clean.py step_03_features.py step_04_eda.py step_05_model.py step_06_report.py; do
        if python3 "$dir/scripts/$step" --data_dir "$dir/data" --output_dir "$dir/output" >> "$LOG" 2>&1; then
            echo "  ✓ $step" | tee -a "$LOG"
        else
            echo "  ✗ $step FAILED (exit=$?)" | tee -a "$LOG"
            ok=0
            break
        fi
    done
    if [ "$ok" -eq 1 ]; then
        echo "  ✓ $dirname COMPLETE" | tee -a "$LOG"
        SUCCESS=$((SUCCESS+1))
    else
        echo "  ✗ $dirname FAILED" | tee -a "$LOG"
        FAILED=$((FAILED+1))
    fi
    echo "" >> "$LOG"
done

echo "" | tee -a "$LOG"
echo "=== SUMMARY: $SUCCESS succeeded, $FAILED failed, $SKIPPED skipped ===" | tee -a "$LOG"
