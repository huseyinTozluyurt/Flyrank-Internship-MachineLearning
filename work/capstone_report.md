# Capstone Report — Prioritizing decline-labeled pages for editorial review

- **Author:** Hüseyin Tozluyurt
- **Lane:** Content-decay detection and prioritization (binary ranking, current label)
- **Repo:** https://github.com/huseyinTozluyurt/Flyrank-Internship-MachineLearning
- **Date:** 26 October 2026
- **Notebook:** [`work/notebooks/capstone.ipynb`](notebooks/capstone.ipynb) · **Metrics receipt:** [`work/outputs/capstone_metrics.json`](outputs/capstone_metrics.json) · **Paper:** [`docs/index.html`](../docs/index.html)

> Every number in this report comes from `work/outputs/capstone_metrics.json`, written by one top-to-bottom run of the capstone notebook.

## 0. Abstract

Can a few observable page signals rank pages so that an editor's 50-page review list holds more pages carrying FlyRank's supplied decline label than the existing "stale and high-traffic" rule, for clients the model has never seen? Using the anonymized 30,000-page, 32-client starter CSV, I compared that rule with logistic regression and random forest on six features, over 20 repeated client-held-out splits, with leakage checks and two sensitivity analyses. Both models beat the rule (Precision@50 0.77 and 0.75 vs 0.66; held-out base rate 0.58; average precision 0.66 and 0.68 vs 0.58), but only the random forest kept its top-50 precision (0.77, base rate 0.55) once 1,205 pages whose missing position data almost always means a `new` label were removed. The output is a client-held-out review queue with plain reason codes, intended as decision support for human editors. It is exploratory ranking of a supplied current label, not early warning and not evidence that editing improves performance.

## 1. Problem framing

- **Decision supported:** which ~50 pages an editor reviews first in a cycle.
- **Unit of analysis:** one page (`content_id`) within a client (`client_id`).
- **Output:** a rank, delivered as a review queue (top 20, next 30, backlog) with reason codes.
- **Human action:** the editor checks context (seasonality, SERP, indexing, intent, accuracy) and decides whether to act. Nothing is changed automatically.
- **Cost of a wrong call:** a false positive spends one review slot; a false negative pushes a decline-labeled page further down the backlog. Review capacity is the binding constraint, so Precision@50 is the operational metric and average precision the overall ranking metric.
- **Why ML:** the existing rule uses two fields. A model can combine several weak signals, but only a held-out comparison against the rule shows whether that helps.

## 2. Data safety

- **Data used:** `data/raw/content_refresh_anonymized.csv` only: 30,000 rows, 44 columns, 30,000 unique pages, 32 pseudonymized clients. All 30,000 rows were eligible (no duplicates, no unrecognized labels).
- **Excluded from features on purpose:** `trend_direction` and `trend_pct` (the label is computed from them), every `*_last_30d` / `*_prev_30d` column and change field (the label arithmetic itself), and `content_id` / `client_id` (grouping only). An assertion in the notebook fails if any of these enters the feature set.
- **Leakage probe:** each allowed feature alone ranks the label with AUC between 0.505 and 0.591; the forbidden `trend_pct` alone gives 1.0. No direct label leak is present.
- **Subtler risks found:**
  - `impressions_90d`, `ctr` and `avg_position` are measured over a 90-day window that contains the 30-day label window, so they can partly reflect the decline itself.
  - The 1,205 pages with `avg_position == 0` are 95.8% labeled `new` (no impressions in the earlier window). Their missing-position flag is a near-mechanical marker of a non-decline label.
- **Public safety:** no client names, URLs, queries, or client IDs appear in `work/`, the notebook outputs, or the paper. Full queues with pseudonymous IDs are written to `work/outputs/*.csv`, which is gitignored.

## 3. Baseline

The existing rule: pages with `days_since_last_update > 180`, ordered by `impressions_90d`; all other pages tie at the bottom. It is a fair comparison because it is what an editor would use today, needs no training, and is scored on the identical held-out rows as the models.

On 20 client-held-out splits it reached **Precision@50 0.66** (lift 1.13 over the base rate) and **average precision 0.58**, equal to the mean held-out base rate of 0.58. Its within-client ranking is at chance (median within-client AUC 0.50): it helps only by choosing which clients' pages rise to the top.

## 4. Model / analysis

- **Target:** `is_declining_label = 1` when `trend_direction == 'down'` (last-30-day impressions more than 20% below the previous 30 days), else 0. Base rate 54.2%.
- **Features (6):** `days_since_last_update`, `content_age_days`, `impressions_90d`, `avg_position` (0 recoded to missing), `ctr`, and `days_since_last_update × avg_position`.
- **Left out on purpose:** label-derived fields and IDs (above); `word_count` / `char_count` (25.7% missing, concentrated by content type); keyword fields (8.2% missing).
- **Models:** logistic regression (class-balanced, standardized) and random forest (200 trees, max depth 5, min leaf 2, class-balanced). Both use median imputation plus missing-value indicators fitted inside each training split.
- **Preprocessing check (Milestone 2):** on five grouped seeds, median plus indicators matched complete-case rows (AP 0.654, Precision@50 0.748) and beat plain median imputation (0.645, 0.676) while keeping every row.
- **Sensitivity models:** (a) logistic regression on the two age fields only, which do not overlap the label window; (b) all candidates re-run without the 1,205 position-missing pages.

## 5. Evaluation

**Split:** 20 repeated 75/25 `GroupShuffleSplit` partitions by `client_id` (seeds 42–61, about 8 held-out clients each). Seeds 42–46 reproduce Milestone 4: logistic regression matches exactly (AP 0.654, Precision@50 0.748) and the forest's AP matches (0.663); its Precision@50 is 0.724 here against 0.708 reported, a tie-breaking difference in the top-50 sort. A stratified random page split is a diagnostic only.

**Main results (mean over 20 client-held-out splits; held-out base rate 0.58):**

| Candidate | Average precision | ROC AUC | P@20 | P@50 | P@100 | Lift@50 |
|---|---|---|---|---|---|---|
| Stale + traffic rule | 0.581 | 0.501 | 0.70 | 0.66 | 0.64 | 1.13 |
| Logistic regression | 0.664 | 0.614 | 0.77 | 0.77 | 0.77 | 1.33 |
| Random forest | 0.683 | 0.638 | 0.75 | 0.75 | 0.77 | 1.31 |
| Age-only logistic (sensitivity) | 0.647 | 0.588 | 0.67 | 0.70 | 0.69 | 1.20 |

**Paired, same splits:** logistic regression beat the rule on Precision@50 in 19 of 20 splits (mean +0.11); the forest in 14 of 20 (+0.09). Both models beat the rule on average precision in 20 of 20. Forest vs logistic: Precision@50 −0.016 (forest higher in 9 of 20), average precision +0.019 (16 of 20).

**Without the 1,205 position-missing pages (28,795 pages, base rate 0.55):**

| Candidate | Average precision | P@50 | Lift@50 |
|---|---|---|---|
| Stale + traffic rule | 0.552 | 0.57 | 1.03 |
| Logistic regression | 0.618 | 0.61 | 1.10 |
| Random forest | 0.668 | 0.77 | 1.41 |
| Age-only logistic | 0.615 | 0.67 | 1.21 |

The forest's Precision@50 was higher than logistic regression's in 18 of 20 splits (mean +0.17).

**Split-design diagnostic (seeds 42–46):** with random page splits, 31.4 of 32 clients appear on both sides, and the forest scores Precision@50 0.85 / AP 0.73 against 0.72 / 0.66 when clients are held out. Random splits overstate transfer to new clients.

**Error analysis:**
- *What fills the misses.* In the pooled top 50, the rule's non-decline picks are mostly `up` (14.9%) and `stable` (14.1%) pages; logistic regression's top 50 holds 7.0% `flat` pages, the forest's almost none (0.1%).
- *Client spread.* Within held-out clients with at least 30 pages, median within-client AUC is 0.55 for logistic regression (4 of 29 clients below 0.5) and 0.61 for the forest (1 of 29 below 0.5). Results depend heavily on which clients are held out: the forest's Precision@50 ranges from 0.52 to 0.98 across the 20 splits (logistic regression: 0.66 to 0.96).
- *Calibration.* Brier scores are 0.234 (logistic) and 0.228 (forest), against 0.25 for a constant 0.5. Scores are usable as ranks, not as probabilities.

## 6. Interpretation

- **Page age carries most of the usable signal.** Older pages are *less* likely to carry the decline label (logistic coefficient for `content_age_days` −0.35), and pages left longer without updates are somewhat more likely (+0.19). The age-only model keeps most of the full model's average precision (0.647 vs 0.664).
- **Missing position is the biggest single logistic signal, and it is an artifact.** Both missing-position indicators have the largest coefficients (−0.53). They mostly tell the model "this page is `new`". This helps pooled metrics by pushing easy negatives down, but does little to order the pages that remain. That is why logistic regression's top-50 edge disappears without those pages.
- **The forest leans on traffic volume and age** (impurity importance 0.35 for `impressions_90d`, 0.21 for `content_age_days`). Traffic volume overlaps the label window, so part of this may reflect the decline itself.
- **Negative results worth keeping:** the existing rule ranks no better than the base rate overall; `ctr`, `avg_position` and the staleness × position interaction add little alone (single-feature AUC ≤ 0.515).
- **Decision changed by the capstone:** Milestone 5 chose logistic regression as the default queue. The capstone switches to random forest because its top-50 precision survives the position-missing sensitivity check and its within-client ranking is more consistent.

## 7. Recommendation

- **Use the random-forest queue as the default review list**, with the logistic queue as a comparison. The queue is built from five client-held-out partitions (seed 42). Each page is scored only by models that never saw its client, and pages are ranked by how often they reach the per-fold top 50, then by mean rank percentile. The two queues share only 5 of their top 50 pages, which is another sign that the ranking is fragile at the page level.
- **How an editor uses it tomorrow:** work `TOP_20_REVIEW`, then `NEXT_30_REVIEW`. Read the reason codes as a checklist: *high visibility* (33 of the top 50) means confirming the traffic drop is real; *position danger band 6–22* (7) means checking the SERP and competing pages; *model priority, context first* (11) means no simple flag fired, so start from context. Before any action, check seasonality, indexing, intent and accuracy. Log what was reviewed and what was done.
- **Spread review across clients.** The forest's top 50 comes from 6 clients, 40% from one. If the queue serves several clients, cap pages per client or run it per client.
- **Never** bulk-edit, delete or redirect from the queue.
- **Confidence:** moderate for "these models order decline-labeled pages better than the current rule on unseen clients, in this snapshot." Low for anything about future declines or the effect of editing. A 50-page queue from the forest averaged about 75–77% decline-labeled pages on held-out clients, against a base rate of 55–58%. Expect roughly one in four reviewed pages not to carry the label.

## 8. Reproducibility

```bash
git clone https://github.com/huseyinTozluyurt/Flyrank-Internship-MachineLearning
cd Flyrank-Internship-MachineLearning
pip install -r requirements.txt jupyter
jupyter nbconvert --to notebook --execute --inplace work/notebooks/capstone.ipynb
```

Or open the notebook in Colab from its badge and choose Runtime → Run all (about 1–3 minutes).

- **Seeds:** grouped evaluation 42–61; queue construction `GroupShuffleSplit(n_splits=5, random_state=42)`; model `random_state` equals the split seed. Seeds 42–46 reproduce Milestone 4.
- **Environment of the recorded run:** Python 3, pandas 3.0.5, numpy 2.5.3, scikit-learn 1.9.1, matplotlib 3.11.2 (also stored in the metrics file).
- **Committed receipts:** `work/outputs/capstone_metrics.json` and the figures in `work/figures/` (copied to `docs/img/`). Review queues are regenerated into `work/outputs/*.csv` and gitignored because they hold row-level pseudonymous IDs.
- **No sealed holdout is claimed.** All evaluation is repeated client-held-out cross-validation on the same snapshot.
- **Not run here:** the DuckDB warehouse validation (Milestone 7). It needs a runtime-only `HF_TOKEN`, and its results would be recorded separately.

## 9. Acknowledgments & data credit

Built on the FlyRank ML Internship dataset: the anonymized content-refresh starter slice provided by [FlyRank](https://flyrank.ai). Thanks to the FlyRank mentors for the data, the problem framing and the internship materials this work builds on.

---

**Limitations (also in the paper):**
1. Current-label task only: no evidence of warning before a decline.
2. Feature windows overlap the label window; feature dates are unverified in the CSV.
3. Only 32 clients, very uneven in size; repeated splits overlap, so spreads are descriptive, not significance tests.
4. Scores are not calibrated probabilities.
5. Reason codes are threshold rules, not causes or per-score explanations.
6. No measured outcomes after editorial review.

**Next steps:** (1) run the DuckDB warehouse validation with dated per-client windows and re-run this evaluation on eligible rows; (2) if dated history allows, run the separate Future Content-Decay Early Warning study with a prior feature window, a later outcome window and time-ordered validation; (3) log editor actions and later outcomes so impact can eventually be measured.
