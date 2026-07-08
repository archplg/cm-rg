"""
Show last 30 calls from state.json with HTTP status codes.
Cost: $0. Helps diagnose what's actually failing.
"""
import json
from pathlib import Path

state_path = Path("results_phase2l/state.json")
if not state_path.exists():
    print(f"ERROR: {state_path} not found")
    exit(1)

state = json.loads(state_path.read_text(encoding="utf-8"))
recent = state.get("recent_activity", [])

print(f"Total cost so far: ${state.get('total_cost_usd', 0):.4f}")
print(f"Total calls:       {state.get('calls_total', 0)}")
print(f"Total errors:      {state.get('errors_count', 0)}")
print()
print("Last 30 calls:")
print(f"  {'time':<10} {'short':<6} phase  {'status':<12} {'cost':>10}  family")
print("-" * 75)
for r in recent[-30:]:
    ts = r.get("ts", "")
    short = r.get("short", "")
    phase = r.get("phase", "")
    status = r.get("status", "")
    cost = r.get("cost_usd", 0)
    slug = r.get("slug", "")
    family = slug.split("/")[0] if slug else ""
    print(f"  {ts:<10} {short:<6} {phase:<5} {str(status):<12} ${cost:>8.4f}  {family}")

# Count statuses
print()
print("Status counts in recent activity:")
from collections import Counter
counts = Counter(r.get("status", "?") for r in recent)
for status, n in counts.most_common():
    print(f"  {status:<15} {n}")

# Per-provider counts of HTTP_0 or HTTP_4xx etc
print()
print("Provider summary (recent activity):")
prov_data = {}
for r in recent:
    slug = r.get("slug", "")
    family = slug.split("/")[0] if slug else "?"
    status = r.get("status", "?")
    if family not in prov_data:
        prov_data[family] = {"OK": 0, "errors": 0}
    if status == "OK":
        prov_data[family]["OK"] += 1
    else:
        prov_data[family]["errors"] += 1
for family, counts in sorted(prov_data.items()):
    print(f"  {family:<15} OK={counts['OK']:<4} errors={counts['errors']}")
