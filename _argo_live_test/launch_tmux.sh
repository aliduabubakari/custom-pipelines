#!/bin/bash
# Launch Argo evaluation in tmux background session
# Usage: ./launch_tmux.sh

SESSION="argo-eval"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Kill existing session if any
tmux kill-session -t "$SESSION" 2>/dev/null || true

# Create new detached session running the orchestrator
tmux new-session -d -s "$SESSION" -c "$SCRIPT_DIR" \
    "bash ${SCRIPT_DIR}/orchestrator.sh 5 1 2>&1 | tee ${SCRIPT_DIR}/../argo_live_results/full_run.log"

echo "=========================================="
echo " Argo evaluation launched in tmux"
echo " Session: $SESSION"
echo "=========================================="
echo ""
echo " Commands:"
echo "   tmux attach -t $SESSION   # View progress"
echo "   Ctrl+B D                  # Detach (leave running)"
echo "   tmux kill-session -t $SESSION  # Stop"
echo ""
echo " Results: $(cd "$SCRIPT_DIR/.." && pwd)/argo_live_results/"
echo " Log:     $(cd "$SCRIPT_DIR/.." && pwd)/argo_live_results/full_run.log"
echo "=========================================="
