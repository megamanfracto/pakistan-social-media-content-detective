"""Compare phone brands after running the notebook once per brand.

Each run must save to its own folder:  OUT_DIR = "outputs/oppo", "outputs/realme", ...
Then:   python compare_brands.py            (add --min-n 150 to change the "enough data" bar)

Writes outputs/brand_comparison.csv and outputs/brand_comparison.png
"""
import argparse, glob, os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

ap = argparse.ArgumentParser()
ap.add_argument("--outputs", default="outputs")
ap.add_argument("--min-n", type=int, default=100, help="brands with fewer comments are flagged as too small to compare")
a = ap.parse_args()

files = sorted(glob.glob(os.path.join(a.outputs, "*", "labeled_comments.csv")))
if not files:
    raise SystemExit("No outputs/<brand>/labeled_comments.csv found.\n"
                     "Run the notebook once per brand with OUT_DIR = 'outputs/<brand>' first.")

frames = []
for f in files:
    d = pd.read_csv(f)
    d["brand"] = os.path.basename(os.path.dirname(f)).title()
    frames.append(d)
df = pd.concat(frames, ignore_index=True)
df["trust_flag"] = df["trust_flag"].astype(str).str.lower().eq("true")


def net(s):
    return ((s == "Positive").sum() - (s == "Negative").sum()) / max(len(s), 1) * 100


rows = []
for brand, g in df.groupby("brand"):
    ex = g.assign(aspect=g["aspects"].fillna("").str.split("; ")).explode("aspect")
    ex = ex[ex["aspect"].fillna("").str.len() > 0]
    t = ex.groupby("aspect")["sentiment"].agg(
        n="size", neg=lambda s: (s == "Negative").mean() * 100, pos=lambda s: (s == "Positive").mean() * 100)
    t = t[t["n"] >= 5]
    rows.append({
        "brand": brand, "n_comments": len(g), "platforms": g["platform"].nunique(),
        "positive_%": (g["sentiment"] == "Positive").mean() * 100,
        "negative_%": (g["sentiment"] == "Negative").mean() * 100,
        "net_sentiment": net(g["sentiment"]),
        "trust_flag_%": g["trust_flag"].mean() * 100,
        "median_engagement": g["engagement"].median(),
        "top_complaint": t["neg"].idxmax() if len(t) else "n/a",
        "top_praise": t["pos"].idxmax() if len(t) else "n/a",
        "enough_data": len(g) >= a.min_n,
    })
res = pd.DataFrame(rows).set_index("brand").sort_values("net_sentiment", ascending=False)
res.round(1).to_csv(os.path.join(a.outputs, "brand_comparison.csv"))
print(res.round(1).to_string())

ok = res.index[res["enough_data"]]
if len(ok) >= 2:
    chi2, p, _, _ = stats.chi2_contingency(pd.crosstab(df[df.brand.isin(ok)]["brand"], df[df.brand.isin(ok)]["sentiment"]))
    print(f"\nSentiment differs between brands (n >= {a.min_n})? chi-square p = {p:.4f}")
small = res.index[~res["enough_data"]].tolist()
if small:
    print(f"\n!! Too few comments to compare fairly (< {a.min_n}): {', '.join(small)}")
print("\nNote: brands are only comparable if collected from a similar mix of platforms and post types.")

fig, ax = plt.subplots(1, 2, figsize=(11, 1.5 + 0.6 * len(res)))
cols = ["#43a047" if v >= 0 else "#e53935" for v in res["net_sentiment"]]
cols = [c if e else "#bdbdbd" for c, e in zip(cols, res["enough_data"])]
ax[0].barh(res.index, res["net_sentiment"], color=cols); ax[0].axvline(0, color="k", lw=.8)
ax[0].set_title("Net sentiment (positive% - negative%)"); ax[0].invert_yaxis()
ax[1].barh(res.index, res["trust_flag_%"], color=["#8e24aa" if e else "#bdbdbd" for e in res["enough_data"]])
ax[1].set_title("Trust / authenticity complaints (% of comments)")
ax[1].invert_yaxis()
fig.suptitle("Phone brands in Pakistan (grey = too few comments)", fontweight="bold")
plt.tight_layout(); plt.savefig(os.path.join(a.outputs, "brand_comparison.png"), dpi=150, bbox_inches="tight")
print(f"\nSaved {a.outputs}/brand_comparison.csv and .png")
