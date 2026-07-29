import json, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

with open("results/optimization_results.json") as f:
    data = json.load(f)

order = ["fibrotic","lung","skin","systemic"]
labels = {"fibrotic":"Fibrotic-\ntargeted","lung":"Inhaled","skin":"Topical","systemic":"Systemic\n(oral)"}
ro = data["route_optima"]
eff   = [ro[k]["eff"] for k in order]
naes  = [ro[k]["n_aes"] for k in order]
score = [ro[k]["score"] for k in order]

x = np.arange(len(order)); w = 0.26
fig, ax1 = plt.subplots(figsize=(8.2,4.6))
# efficacy and score on left axis (0-100)
b1 = ax1.bar(x - w, eff,   w, label="Predicted efficacy", color="#3B6FB6")
b3 = ax1.bar(x + 0,  score, w, label="Design score",      color="#2F9E44")
ax1.set_ylabel("Efficacy / design score (0–100)")
ax1.set_ylim(0, 110)
ax1.set_xticks(x); ax1.set_xticklabels([labels[k] for k in order])
# adverse-effect count on right axis
ax2 = ax1.twinx()
b2 = ax2.bar(x + w, naes, w, label="Adverse effects (count)", color="#C4392F")
ax2.set_ylabel("Active adverse effects (count)")
ax2.set_ylim(0, max(naes)+2)

for b in b1: ax1.text(b.get_x()+b.get_width()/2, b.get_height()+1.5, f"{int(b.get_height())}", ha="center", fontsize=9, color="#3B6FB6")
for b in b3: ax1.text(b.get_x()+b.get_width()/2, b.get_height()+1.5, f"{int(b.get_height())}", ha="center", fontsize=9, color="#2F9E44")
for b in b2: ax2.text(b.get_x()+b.get_width()/2, b.get_height()+0.08, f"{int(b.get_height())}", ha="center", fontsize=9, color="#C4392F")

lines = [b1, b3, b2]
ax1.legend(lines, [l.get_label() for l in lines], loc="upper center", ncol=3, frameon=False, bbox_to_anchor=(0.5, 1.13))
ax1.set_title("Optimal anti-fibrotic design per delivery route", pad=28, fontsize=12, weight="bold")
for s in ["top"]: ax1.spines[s].set_visible(False); ax2.spines[s].set_visible(False)
plt.tight_layout()
plt.savefig("results/optimization_figure.png", dpi=150, bbox_inches="tight")
print("saved optimization_figure.png")
