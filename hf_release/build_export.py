#!/usr/bin/env python3
"""Export Phase 2L (Case 1, 36 models) to HuggingFace parquet tables.

Replicates the rating-record logic of analyze_phase2l.py::build_long_format
exactly so the row count matches the canonical analysis_results.json
(3,055,153 ratings / 13,928 pairs).
"""
import json, glob, os
import pyarrow as pa
import pyarrow.parquet as pq

ROOT = "/sessions/admiring-laughing-hopper/mnt/archipelago_cross_model/results_phase2l"
OUT = "/sessions/admiring-laughing-hopper/mnt/outputs/hf_phase2l/data"
os.makedirs(OUT, exist_ok=True)

META = json.load(open(f"{ROOT}/analysis_results.json"))["model_meta"]  # short -> {family,tier,name}

def cells_iter(phase):
    for fp in glob.glob(f"{ROOT}/{phase}/*/*/*.json"):
        if "_backups" in fp.split(os.sep):
            continue
        try:
            yield fp, json.loads(open(fp, encoding="utf-8").read())
        except Exception:
            continue

# ---- constructs registry + ratings (replicates build_long_format) ----
constructs = []                 # rows for constructs.parquet
cidx = {}                       # (task,cond,rater,batch,local_idx) -> construct_id
ratings = {c: [] for c in
           ["rating_id","task","condition","rater","ratee",
            "rater_family","rater_tier","ratee_family","ratee_tier",
            "batch","construct_id","rating"]}
rid = 0
for fp, d in cells_iter("phase4_ratings"):
    if d.get("ok_batches", 0) == 0:
        continue
    rater = d.get("rater_short")
    if not rater or rater not in META:
        continue
    task = d.get("task"); cond = d.get("condition")
    rated = d.get("rated_responses") or []
    rf = META[rater]["family"]; rt = META[rater]["tier"]
    for batch in d.get("batches", []) or []:
        if batch.get("parse_error"):
            continue
        rows = batch.get("ratings") or []
        cons = batch.get("constructs") or []
        b = batch.get("batch", 0)
        for resp_i, row in enumerate(rows):
            if resp_i >= len(rated) or not isinstance(row, list):
                continue
            ratee = rated[resp_i]
            em = META.get(ratee, {})
            for ci, val in enumerate(row):
                if ci >= len(cons) or not isinstance(val, (int, float)):
                    continue
                r = int(val)
                if r < 1 or r > 7:
                    continue
                key = (task, cond, rater, b, ci)
                gid = cidx.get(key)
                if gid is None:
                    gid = len(constructs)
                    cidx[key] = gid
                    con = cons[ci]
                    constructs.append({
                        "construct_id": gid, "task": task, "condition": cond,
                        "rater": rater, "batch": b, "construct_local_idx": ci,
                        "pole_a": con.get("pole_a", ""), "pole_b": con.get("pole_b", ""),
                        "context": con.get("context", ""), "from_rater": con.get("from_rater", rater),
                    })
                ratings["rating_id"].append(rid)
                ratings["task"].append(task); ratings["condition"].append(cond)
                ratings["rater"].append(rater); ratings["ratee"].append(ratee)
                ratings["rater_family"].append(rf); ratings["rater_tier"].append(rt)
                ratings["ratee_family"].append(em.get("family")); ratings["ratee_tier"].append(em.get("tier"))
                ratings["batch"].append(b); ratings["construct_id"].append(gid)
                ratings["rating"].append(r)
                rid += 1

# ---- responses (phase1) + anonymized (phase2) ----
anon = {}
for fp, d in cells_iter("phase2_anonymized"):
    anon[(d.get("task"), d.get("condition"), d.get("short_name"))] = d.get("anonymized_text", "")
resp = {c: [] for c in ["response_id","task","condition","model","model_slug",
                        "family","tier","persona","response","anonymized_text",
                        "cost_usd","latency_ms","timestamp"]}
i = 0
for fp, d in cells_iter("phase1_free_response"):
    t, c, m = d.get("task"), d.get("condition"), d.get("short_name")
    resp["response_id"].append(i); resp["task"].append(t); resp["condition"].append(c)
    resp["model"].append(m); resp["model_slug"].append(d.get("model_slug"))
    resp["family"].append(d.get("family")); resp["tier"].append(d.get("tier"))
    resp["persona"].append(d.get("persona")); resp["response"].append(d.get("response", ""))
    resp["anonymized_text"].append(anon.get((t, c, m), ""))
    resp["cost_usd"].append(d.get("cost_usd")); resp["latency_ms"].append(d.get("latency_ms"))
    resp["timestamp"].append(d.get("timestamp"))
    i += 1

# ---- cells (per phase4 file) ----
cells = {c: [] for c in ["cell_id","task","condition","rater","rater_slug","family","tier",
                         "n_batches","ok_batches","n_constructs_total","total_cost_usd",
                         "total_latency_ms","timestamp"]}
j = 0
for fp, d in cells_iter("phase4_ratings"):
    if d.get("ok_batches", 0) == 0:
        continue
    cells["cell_id"].append(j); cells["task"].append(d.get("task")); cells["condition"].append(d.get("condition"))
    cells["rater"].append(d.get("rater_short")); cells["rater_slug"].append(d.get("rater_slug"))
    cells["family"].append(d.get("rater_family")); cells["tier"].append(d.get("rater_tier"))
    cells["n_batches"].append(d.get("n_batches")); cells["ok_batches"].append(d.get("ok_batches"))
    cells["n_constructs_total"].append(d.get("n_constructs_total"))
    cells["total_cost_usd"].append(d.get("total_cost_usd")); cells["total_latency_ms"].append(d.get("total_latency_ms"))
    cells["timestamp"].append(d.get("timestamp"))
    j += 1

# ---- api_calls (phases 1, 3, 4) ----
api = {c: [] for c in ["call_id","phase","task","condition","model","cost_usd","latency_ms","timestamp"]}
k = 0
def add_call(phase, t, c, m, cost, lat, ts):
    global k
    api["call_id"].append(k); api["phase"].append(phase); api["task"].append(t)
    api["condition"].append(c); api["model"].append(m); api["cost_usd"].append(cost)
    api["latency_ms"].append(lat); api["timestamp"].append(ts); k += 1
for fp, d in cells_iter("phase1_free_response"):
    add_call("phase1", d.get("task"), d.get("condition"), d.get("short_name"), d.get("cost_usd"), d.get("latency_ms"), d.get("timestamp"))
for fp, d in cells_iter("phase3_constructs"):
    add_call("phase3", d.get("task"), d.get("condition"), d.get("rater_short"), d.get("cost_usd"), d.get("latency_ms"), d.get("timestamp"))
for fp, d in cells_iter("phase4_ratings"):
    add_call("phase4", d.get("task"), d.get("condition"), d.get("rater_short"), d.get("total_cost_usd"), d.get("total_latency_ms"), d.get("timestamp"))

# ---- write ----
def write(name, table):
    pq.write_table(pa.table(table), f"{OUT}/{name}.parquet", compression="zstd")
write("ratings", ratings)
write("constructs", {c: [r[c] for r in constructs] for c in constructs[0]})
write("responses", resp)
write("cells", cells)
write("api_calls", api)

# ---- summary for verification ----
pairs = len({(t,c,ra,re) for t,c,ra,re in zip(ratings["task"],ratings["condition"],ratings["rater"],ratings["ratee"])})
total_cost = sum(x for x in api["cost_usd"] if x)
print("ratings:", len(ratings["rating_id"]))
print("unique pairs:", pairs)
print("constructs(table rows):", len(constructs))
print("responses:", len(resp["response_id"]))
print("cells:", len(cells["cell_id"]))
print("api_calls:", len(api["call_id"]), "total_cost_usd: %.2f" % total_cost)
