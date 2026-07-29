"""
Reproducible optimization for the anti-fibrotic placeholder design model.
Exhaustively searches every therapeutic-target subset x delivery localization,
scoring predicted efficacy vs adverse-effect penalty, and reports the optimum
per delivery route. Illustrative heuristic weights (see notes) — the STRUCTURE
of the result is the finding, not the exact numbers.
"""
import json, itertools

SEVW = {"serious": 25, "moderate": 10, "low": 3}
# therapeutic targets: efficacy weight + adverse effects [(label, tissue, severity)]
THER = {
 "YAP":  (40, [("GI epithelial toxicity","gi","serious"),("Immunosuppression","immune","moderate"),("Impaired wound healing","fibrotic","moderate")]),
 "SRC":  (30, [("Bleeding","platelets","serious"),("PAH","pulmendo","serious"),("Pleural effusion","pulmendo","serious")]),
 "MEK":  (30, [("Retinopathy","retina","serious"),("Rash","skin","moderate"),("LVEF drop","cardiac","moderate"),("CK elevation","muscle","low"),("Diarrhea","gi","low"),("Neurologic","cns","moderate")]),
 "FAK":  (30, [("GI toxicity","gi","moderate"),("Hematologic","marrow","low")]),
 "ROCK2":(25, [("Infection/immunosuppression","immune","moderate"),("Nausea/diarrhea","gi","low")]),
 "PDGFR":(20, [("Fluid retention/edema","vasc","moderate")]),
 "DDR1": (20, [("Mild epithelial effects","gi","low")]),
}
ALL_TISSUES = ["fibrotic","pulmendo","platelets","marrow","immune","cardiac","retina","skin","muscle","gi","cns","vasc"]
LOC = {"systemic": ALL_TISSUES, "lung": ["fibrotic","pulmendo"], "skin": ["fibrotic","skin"], "fibrotic": ["fibrotic"]}
REV_THRESHOLD = 40

def evaluate(hit, loc):
    reach = set(LOC[loc])
    eff = min(100, sum(THER[t][0] for t in hit))
    active = {}
    for t in hit:
        for label, tissue, sev in THER[t][1]:
            if tissue in reach:
                if label not in active or SEVW[sev] > SEVW[active[label]]:
                    active[label] = sev
    penalty = sum(SEVW[s] for s in active.values())
    score = max(0, eff - penalty)
    n_serious = sum(1 for s in active.values() if s == "serious")
    return dict(eff=eff, reversal=eff >= REV_THRESHOLD, aes=active,
                n_aes=len(active), n_serious=n_serious, penalty=penalty, score=score)

targets = list(THER)
results = []
for r in range(1, len(targets)+1):
    for hit in itertools.combinations(targets, r):
        for loc in LOC:
            e = evaluate(hit, loc)
            results.append(dict(hit=list(hit), loc=loc, **e))

def best(pred, key):
    c = [x for x in results if pred(x)]
    return max(c, key=key) if c else None

print("Global best design score:")
g = best(lambda x: True, lambda x: (x["score"], -len(x["hit"])))
print(" ", "+".join(g["hit"]), "|", g["loc"], "| eff", g["eff"], "| AEs", g["n_aes"], "| score", g["score"])

print("\nBest per delivery route (max score, reversal achieved):")
route_best = {}
for loc in LOC:
    b = best(lambda x: x["loc"] == loc and x["reversal"], lambda x: (x["score"], -x["n_aes"], -len(x["hit"])))
    route_best[loc] = b
    print(f"  {loc:9s}: {'+'.join(b['hit']):24s} eff {b['eff']:3d}  AEs {b['n_aes']} ({b['n_serious']} serious)  score {b['score']}")

print("\nZero-AE reachability by route:")
for loc in LOC:
    z = best(lambda x: x["loc"] == loc and x["n_aes"] == 0, lambda x: (x["eff"], -len(x["hit"])))
    print(f"  {loc:9s}: {'eff '+str(z['eff'])+' via '+'+'.join(z['hit']) if z else 'no zero-AE design exists'}")

# save machine-readable summary
summary = {loc: {"hit": b["hit"], "eff": b["eff"], "n_aes": b["n_aes"],
                 "n_serious": b["n_serious"], "score": b["score"],
                 "adverse_effects": b["aes"]} for loc, b in route_best.items()}
with open("results/optimization_results.json", "w") as f:
    json.dump({"global_best": {"hit": g["hit"], "loc": g["loc"], "score": g["score"]},
               "route_optima": summary, "n_designs_evaluated": len(results)}, f, indent=2)
print(f"\nEvaluated {len(results)} designs. Saved optimization_results.json")
