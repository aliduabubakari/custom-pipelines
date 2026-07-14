#!/usr/bin/env python3
"""Aggregate Argo workflow evaluation results into a summary report."""
import json, os, glob
from collections import defaultdict
from datetime import datetime

EVAL_DIR = "/Users/abubakarialidu/Downloads/custom_pipelines/argo_workflow_evaluations"
OUT_DIR = EVAL_DIR

results = []
for f in sorted(glob.glob(os.path.join(EVAL_DIR, "*.json"))):
    # Skip summary files and "full" variant
    basename_check = os.path.basename(f)
    if "_full.json" in basename_check or "SUMMARY" in basename_check:
        continue
    with open(f) as fh:
        data = json.load(fh)
    basename = os.path.splitext(os.path.basename(f))[0]
    # Extract pipeline number and name
    parts = basename.split("_", 1)
    num = parts[0]
    name = parts[1] if len(parts) > 1 else basename

    summary = data.get("summary", {})
    sat_data = data.get("static_analysis", {})
    pct_data = data.get("platform_compliance", {})

    sat_scores = sat_data.get("scores", {}) if isinstance(sat_data, dict) else {}
    pct_scores = pct_data.get("scores", {}) if isinstance(pct_data, dict) else {}
    pct_meta = pct_data.get("metadata", {}) if isinstance(pct_data, dict) else {}

    conformance = pct_meta.get("conformance_stack", {})
    argo_lint = pct_meta.get("argo_lint", {})

    results.append({
        "num": num,
        "name": name,
        "combined": summary.get("combined_score"),
        "sat": summary.get("static_score"),
        "pct": summary.get("compliance_score"),
        "gates_passed": summary.get("platform_gate_passed"),
        "sat_correctness": sat_scores.get("correctness", {}).get("raw_score"),
        "sat_code_quality": sat_scores.get("code_quality", {}).get("raw_score"),
        "sat_best_practices": sat_scores.get("best_practices", {}).get("raw_score"),
        "sat_maintainability": sat_scores.get("maintainability", {}).get("raw_score"),
        "sat_robustness": sat_scores.get("robustness", {}).get("raw_score"),
        "pct_loadability": pct_scores.get("loadability", {}).get("raw_score"),
        "pct_structure": pct_scores.get("structure_validity", {}).get("raw_score"),
        "pct_config": pct_scores.get("configuration_validity", {}).get("raw_score"),
        "pct_task": pct_scores.get("task_validity", {}).get("raw_score"),
        "pct_executability": pct_scores.get("executability", {}).get("raw_score"),
        "argo_lint": argo_lint.get("status"),
        "hydration_tasks": conformance.get("hydration", {}).get("task_count", 0),
        "script_compile_ok": conformance.get("script_compile", {}).get("ok"),
        "template_count": pct_meta.get("template_count", 0),
        "file_size": pct_meta.get("file_size_bytes", 0),
        "issues": len(data.get("static_analysis", {}).get("issues", [])) + len(data.get("platform_compliance", {}).get("issues", [])),
    })

# Sort by number
results.sort(key=lambda r: int(r["num"]))

# Generate report
report = []
report.append("=" * 100)
report.append(f"ARGO WORKFLOW EXECUTABILITY REPORT")
report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
report.append(f"Total pipelines evaluated: {len(results)}")
report.append(f"Argo CLI: v4.0.6 (argo lint --offline --strict)")
report.append("=" * 100)

# Overall stats
gates_ok = sum(1 for r in results if r["gates_passed"])
avg_combined = sum(r["combined"] for r in results if r["combined"]) / len(results)
avg_sat = sum(r["sat"] for r in results if r["sat"]) / len(results)
avg_pct = sum(r["pct"] for r in results if r["pct"]) / len(results)
lint_ok = sum(1 for r in results if r["argo_lint"] == "passed")
total_issues = sum(r["issues"] for r in results)

report.append(f"\n## OVERALL STATISTICS")
report.append(f"  Gates passed:      {gates_ok}/{len(results)} ({gates_ok/len(results)*100:.0f}%)")
report.append(f"  Argo lint passed:  {lint_ok}/{len(results)} ({lint_ok/len(results)*100:.0f}%)")
report.append(f"  Avg Combined Score: {avg_combined:.2f}/10")
report.append(f"  Avg SAT Score:      {avg_sat:.2f}/10")
report.append(f"  Avg PCT Score:      {avg_pct:.2f}/10")
report.append(f"  Total issues:       {total_issues}")

# Dimension averages
sat_dims = ["sat_correctness", "sat_code_quality", "sat_best_practices", "sat_maintainability", "sat_robustness"]
pct_dims = ["pct_loadability", "pct_structure", "pct_config", "pct_task", "pct_executability"]

report.append(f"\n## SAT DIMENSION AVERAGES")
for dim in sat_dims:
    vals = [r[dim] for r in results if r[dim] is not None]
    avg = sum(vals) / len(vals) if vals else 0
    report.append(f"  {dim.replace('sat_',''):20s}: {avg:.2f}/10")

report.append(f"\n## PCT DIMENSION AVERAGES")
for dim in pct_dims:
    vals = [r[dim] for r in results if r[dim] is not None]
    avg = sum(vals) / len(vals) if vals else 0
    report.append(f"  {dim.replace('pct_',''):20s}: {avg:.2f}/10")

# Domain breakdown
domain_scores = defaultdict(list)
for r in results:
    if "analytics" in r["name"]:
        dom = "analytics"
    elif "credit" in r["name"] or "customer" in r["name"] or "demand" in r["name"] or "ecommerce" in r["name"] or "employee" in r["name"] or "energy" in r["name"] or "healthcare" in r["name"] or "insurance" in r["name"] or "predictive" in r["name"] or "student" in r["name"]:
        dom = "general_ml"
    elif "hr" in r["name"]:
        dom = "hr"
    elif "sports" in r["name"]:
        dom = "sports"
    elif "transportation" in r["name"]:
        dom = "transportation"
    else:
        dom = "other"
    if r["combined"]:
        domain_scores[dom].append(r["combined"])

report.append(f"\n## BY DOMAIN")
for dom in sorted(domain_scores):
    vals = domain_scores[dom]
    report.append(f"  {dom:20s}: {len(vals):3d} pipelines, avg {sum(vals)/len(vals):.2f}/10")

# Top/bottom 5
report.append(f"\n## TOP 5 PIPELINES (by Combined Score)")
top5 = sorted(results, key=lambda r: r["combined"] or 0, reverse=True)[:5]
for r in top5:
    report.append(f"  {r['num']}_{r['name'][:60]:60s} Combined: {r['combined']:.2f}  SAT: {r['sat']:.2f}  PCT: {r['pct']:.2f}")

report.append(f"\n## BOTTOM 5 PIPELINES (by Combined Score)")
bot5 = sorted(results, key=lambda r: r["combined"] or 10)[:5]
for r in bot5:
    report.append(f"  {r['num']}_{r['name'][:60]:60s} Combined: {r['combined']:.2f}  SAT: {r['sat']:.2f}  PCT: {r['pct']:.2f}")

# Gates failed (if any)
gates_failed = [r for r in results if not r["gates_passed"]]
if gates_failed:
    report.append(f"\n## PIPELINES WITH FAILED GATES ({len(gates_failed)})")
    for r in gates_failed:
        report.append(f"  {r['num']}_{r['name']}")

# Detailed table
report.append(f"\n## FULL TABLE")
report.append(f"{'#':>4s} {'Pipeline':55s} {'Comb':>5s} {'SAT':>5s} {'PCT':>5s} {'Gates':>5s} {'Lint':>6s} {'Tasks':>5s} {'Issues':>6s}")
report.append("-" * 100)
for r in results:
    lint_status = "PASS" if r["argo_lint"] == "passed" else r["argo_lint"] or "N/A"
    gates = "PASS" if r["gates_passed"] else "FAIL"
    report.append(f"{r['num']:>4s} {r['name'][:54]:54s} {r['combined'] or 0:>5.2f} {r['sat'] or 0:>5.2f} {r['pct'] or 0:>5.2f} {gates:>5s} {lint_status:>6s} {r['hydration_tasks']:>5d} {r['issues']:>6d}")

report.append("")
report.append("=" * 100)
report.append("END OF REPORT")

report_text = "\n".join(report)
report_path = os.path.join(OUT_DIR, "SUMMARY_REPORT.txt")
with open(report_path, "w") as f:
    f.write(report_text)

print(report_text)

# Also save as JSON
json_path = os.path.join(OUT_DIR, "SUMMARY_REPORT.json")
with open(json_path, "w") as f:
    json.dump(results, f, indent=2, default=str)
print(f"\nJSON saved: {json_path}")
print(f"Report saved: {report_path}")
