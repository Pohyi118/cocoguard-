"""Competitor positioning map + competitor analysis graph, scored from the capability table on the
'Existing Tools and Competitive Position' page (Yes = 2, Partly = 1, No = 0)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

plt.rcParams["font.family"] = "Segoe UI"
G, G2, G3, MUT, LINE, RED = "#2B654F", "#8CAE9E", "#C9DCD2", "#5f6b65", "#d7e0db", "#A2472E"

# ---------- Figure 1: market competitor map ----------
fig, ax = plt.subplots(figsize=(8.6, 4.6), dpi=200)
ax.set_xlim(0, 10); ax.set_ylim(0, 10)
ax.add_patch(Rectangle((5, 5), 5, 5, color="#eef3ef", zorder=0))
ax.axvline(5, color=LINE, lw=1, zorder=1); ax.axhline(5, color=LINE, lw=1, zorder=1)
ax.text(9.85, 9.7, "Weather-triggered field action\n(the gap KokoShield targets)", ha="right", va="top", fontsize=8.5, color=G, fontweight="bold")
ax.text(0.15, 9.7, "Weather insight, no field plan", ha="left", va="top", fontsize=8, color=MUT)
ax.text(0.15, 0.3, "Records and general advice", ha="left", va="bottom", fontsize=8, color=MUT)
ax.text(9.85, 0.3, "Field tools without a weather trigger", ha="right", va="bottom", fontsize=8, color=MUT)

pts = [  # name, x = field-action specificity, y = weather/climate trigger, offset
    ("Usual round and paper log", 3.2, 1.3, (8, 6)),
    ("Spreadsheet records", 4.0, 3.2, (8, 6)),
    ("Weather forecast models", 1.6, 8.0, (8, -14)),
    ("Plantix photo diagnosis", 6.6, 1.6, (8, 6)),
    ("PlantwisePlus factsheets", 1.4, 2.4, (8, 6)),
]
for n, x, y, off in pts:
    ax.scatter(x, y, s=170, color=G2, edgecolor="white", lw=1.5, zorder=3)
    ax.annotate(n, (x, y), xytext=off, textcoords="offset points", fontsize=8.5, color="#1f2421")
ax.scatter(8.6, 8.2, s=420, color=G, edgecolor="white", lw=2, zorder=4)
ax.annotate("KokoShield", (8.6, 8.2), xytext=(-12, -26), textcoords="offset points", fontsize=10, fontweight="bold", color=G, ha="center")

ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values(): s.set_color(LINE)
ax.set_xlabel("Field-action specificity  →  (general advice … block-level, time-limited route)", fontsize=8.5, color=MUT)
ax.set_ylabel("Weather / climate trigger  →", fontsize=8.5, color=MUT)
plt.tight_layout(); plt.savefig("img/fig_comp_map.png"); plt.close()

# ---------- Figure 2: competitor analysis (stacked capability score) ----------
tools = ["KokoShield (planned)", "Usual round and paper log", "Spreadsheet records", "Plantix", "Weather forecast models", "PlantwisePlus"]
plan = [6, 0, 1, 0, 2, 0]      # rain trigger + ranks blocks + time budget  (max 6)
capture = [3, 2, 1, 3, 0, 2]   # works offline + photo identification       (max 4)
verify = [6, 1, 1, 0, 0, 0]    # adviser confirmation + misses/finds per hour + sponsor report (max 6)
fig, ax = plt.subplots(figsize=(8.6, 3.5), dpi=200)
y = range(len(tools))
ax.barh(y, plan, color=G, height=0.6, label="Trigger and route planning (max 6)")
ax.barh(y, capture, left=plan, color=G2, height=0.6, label="Field capture and diagnosis (max 4)")
ax.barh(y, verify, left=[a + b for a, b in zip(plan, capture)], color=G3, height=0.6, label="Verification and reporting (max 6)")
for i, (a, b, c) in enumerate(zip(plan, capture, verify)):
    ax.text(a + b + c + 0.2, i, f"{a+b+c} / 16", va="center", fontsize=9, fontweight="bold", color="#1f2421")
ax.set_yticks(list(y)); ax.set_yticklabels(tools, fontsize=9)
ax.get_yticklabels()[0].set_fontweight("bold"); ax.get_yticklabels()[0].set_color(G)
ax.invert_yaxis(); ax.set_xlim(0, 17.5)
ax.set_xlabel("Capability score (Yes = 2, Partly = 1, No = 0 across 8 capabilities)", fontsize=8.5, color=MUT)
for s in ["top", "right", "left"]: ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color(LINE); ax.tick_params(colors=MUT, length=0)
ax.grid(axis="x", color="#e6ece9"); ax.set_axisbelow(True)
ax.legend(loc="lower right", fontsize=8, frameon=False)
plt.tight_layout(); plt.savefig("img/fig_comp_scores.png"); plt.close()
print("ok")
