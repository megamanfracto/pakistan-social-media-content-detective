# 🇵🇰 Pakistani Social Media Content Detective

**Business question:** what do Pakistani social-media audiences say about Chinese phone brands (Oppo, Realme, Infinix, Xiaomi, Vivo, Tecno), what drives their engagement and distrust, and what should a brand post next?

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/YOUR-USERNAME/pakistani-social-media-content-detective/blob/main/Pakistani_Phone_Brand_Perception_Pipeline.ipynb)

> After pushing, replace `YOUR-USERNAME` in the badge link with your GitHub username.

## What's in this repo

| File | Purpose |
|---|---|
| `Pakistani_Phone_Brand_Perception_Pipeline.ipynb` | Comments → cleaning → sentiment / aspects / trust flag → 10 charts → AI recommendation → report draft |
| `comments_template.csv` | Column format for your own comments (delete the 3 example rows) |
| `compare_brands.py` | Joins the per-brand runs into one comparison table and chart |
| `outputs/` | Results. Comment-level CSVs are git-ignored |

## How the notebook answers the brief

| Brief question | Where | Caveat |
|---|---|---|
| Which platform performs better? | Charts 1–2, platform table | Comment-level sentiment and engagement, not post reach |
| Which content type gets more engagement? | Chart 6 | `post_type` is the type of post the comment sits under |
| Popular topics / hashtags? | Charts 3–4 | 10 phone aspects; hashtags are not extracted |
| What sentiment drives engagement? | Chart 5 + Kruskal–Wallis test | |
| Best time / day? | Chart 7, day-of-week table | Shows when people comment, not when posts perform best |
| Which audience segment responds more? | Chart 9 | Language only (English / Roman Urdu / Urdu script) |
| What should a brand post next? | Cell 7 | AI prompt (or API call) plus your own critique |

## Quick start

1. Open the notebook in Colab (badge above) or locally: `pip install -r requirements.txt` then `jupyter notebook`.
2. In cell 1 set `BRAND`, `SOURCE` (`youtube`, `paste`, `csv`) and your data path.
3. Run all cells. Charts, tables and `report_draft.md` land in `OUT_DIR`.
4. Hand-label 150 comments (cell 5) to get accuracy and Cohen's kappa.

`SOURCE = "demo"` generates **fake** comments to test the pipeline. Never report demo results.

## Compare several brands

Run the notebook once per brand, each with its own output folder:

```python
BRAND = "Oppo"
SOURCE = "csv"
CSV_PATH = "comments_oppo.csv"
OUT_DIR = "outputs/oppo"
```

Repeat for Realme, Infinix, Xiaomi (and Vivo / Tecno, which are large in Pakistan), then:

```bash
python compare_brands.py
```

This writes `outputs/brand_comparison.csv` and `.png`. Brands with fewer than 100 comments are greyed out and flagged. Aim for 300+ per brand, collected from a similar mix of platforms, or the comparison is unfair.

## Data and safety rules

- Public posts only. Do not store usernames.
- Do not commit raw comment files (`.gitignore` already blocks `comments_*.csv` and comment-level outputs). Keep the repo private if unsure.
- **Never commit API keys.** Cell 1 has `YOUTUBE_API_KEY` and `ANTHROPIC_API_KEY`; clear them before every commit.

## Limitations

- People with problems comment more, so negativity may be overstated.
- Paid or fake comments, sarcasm and Roman Urdu spelling variation can mislead the rule-based labels.
- Samples are not representative of all buyers; no causal claims.
