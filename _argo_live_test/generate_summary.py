#!/usr/bin/env python3
"""Generate master summary from per-pipeline argo_live_results."""
import json, os, glob
from collections import Counter
from datetime import datetime

RESULTS_DIR = "/Users/abubakarialidu/Downloads/custom_pipelines/argo_live_results"

metrics = []
for pipe_dir in sorted(glob.glob(os.path.join(RESULTS_DIR, "*/"))):
    metrics_file = os.path.join(pipe_dir, "metrics.json")
    if os.path.exists(metrics_file):
        with open(metrics_file) as f:
            try:
                m = json.load(f)
                metrics.append(m)
            except:
                pass

total = len(metrics)
if total == 0:
    print("No results found yet.")
    exit(0)

phases = Counter(m.get("phase") for m in metrics)
success = phases.get("Succeeded", 0)
failed = phases.get("Failed", 0)
error = phases.get("Error", 0)
timeout = phases.get("Timeout", 0)
build_fail = sum(1 for m in metrics if m.get("phase") in ("BUILD_FAIL", "SUBMIT_FAIL", "NO_IMAGE"))

durations = [m.get("elapsed_s", 0) for m in metrics if m.get("phase") == "Succeeded"]
steps_ok = sum(m.get("steps_succeeded", 0) for m in metrics)
steps_total = sum(m.get("step_count", 0) for m in metrics)

# Build report
lines = []
lines.append("=" * 90)
lines.append(f"ARGO LIVE EXECUTION REPORT")
lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
lines.append(f"Pipelines tested: {total}")
lines.append("=" * 90)
lines.append("")
lines.append("## Results Summary")
lines.append(f"  ✅ Succeeded:   {success:>3} ({success/total*100:.0f}%)" if total else "")
lines.append(f"  ❌ Failed:      {failed:>3} ({failed/total*100:.0f}%)" if total else "")
lines.append(f"  ⚠️  Error:       {error:>3}" if error else "")
lines.append(f"  ⏰ Timeout:     {timeout:>3}" if timeout else "")
lines.append(f"  🔧 Build/Submit:{build_fail:>3}" if build_fail else "")
lines.append("")
lines.append("## Durations (successful pipelines)")
if durations:
    lines.append(f"  Average: {sum(durations)/len(durations):.0f}s")
    lines.append(f"  Min:     {min(durations):.0f}s")
    lines.append(f"  Max:     {max(durations):.0f}s")
lines.append("")
lines.append(f"## Steps: {steps_ok}/{steps_total} passed ({steps_ok/steps_total*100:.0f}%)" if steps_total else "")

# Domain breakdown
domain_scores = {}
for m in metrics:
    name = m.get("pipeline", "")
    if "analytics" in name: dom = "analytics"
    elif any(k in name for k in ["credit", "customer", "demand", "ecommerce", "employee", "energy", "healthcare", "insurance", "predictive", "student"]): dom = "general-ml"
    elif "hr" in name: dom = "hr"
    elif "sports" in name: dom = "sports"
    elif "transportation" in name: dom = "transportation"
    else: dom = "other"
    if dom not in domain_scores: domain_scores[dom] = {"total": 0, "success": 0}
    domain_scores[dom]["total"] += 1
    if m.get("phase") == "Succeeded": domain_scores[dom]["success"] += 1

lines.append("")
lines.append("## By Domain")
for dom in sorted(domain_scores):
    d = domain_scores[dom]
    rate = f"{d['success']/d['total']*100:.0f}%" if d['total'] else "0%"
    lines.append(f"  {dom:20s}: {d['success']}/{d['total']} succeeded ({rate})")

# Detailed table
lines.append("")
lines.append(f" {'#':>4s} {'Pipeline':48s} {'Phase':>10s} {'Dur':>5s} {'Steps':>7s} {'CPU·s':>6s} {'MB·s':>6s}")
lines.append("-" * 90)
for m in sorted(metrics, key=lambda x: x.get("pipeline", "")):
    name = m.get("pipeline", "?")
    phase = m.get("phase", "?")
    dur = m.get("elapsed_s", 0)
    steps_str = f"{m.get('steps_succeeded',0)}/{m.get('step_count',0)}"
    cpu = m.get("cpu_seconds", 0)
    mem = m.get("memory_mb_seconds", 0)
    icon = "✅" if phase == "Succeeded" else "❌" if phase == "Failed" else "⚠️"
    lines.append(f" {icon} {name[:47]:47s} {phase:>10s} {dur:>4.0f}s {steps_str:>7s} {cpu:>5.0f} {mem:>5.0f}")

lines.append("")
lines.append("=" * 90)

report = "\n".join(lines)
print(report)

# Save
with open(os.path.join(RESULTS_DIR, "SUMMARY.txt"), "w") as f:
    f.write(report)
print(f"\nReport saved to: {RESULTS_DIR}/SUMMARY.txt")
