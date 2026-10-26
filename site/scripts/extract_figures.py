"""Copy the charts used by the site out of the notebooks' saved outputs.

Each entry is (output file, notebook, cell index, n-th image in that cell).
Notebooks are not re-run: the site shows exactly what each notebook recorded.
Figures that show client identifiers on an axis or legend are deliberately
left out of this list.
"""
import base64
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "site" / "public" / "figures"
NB = "notebooks"
REC = "notebooks/ContentRefreshRecommendationEngine"

FIGURES = {
    "eda": [
        ("core-correlation.png", f"{NB}/ExploratoryDataAnalysis.ipynb", 6, 0),
        ("distributions.png", f"{NB}/ExploratoryDataAnalysis.ipynb", 8, 0),
        ("decline-by-position.png", f"{NB}/ExploratoryDataAnalysis.ipynb", 9, 0),
        ("label-correlation.png", f"{NB}/ExploratoryDataAnalysis.ipynb", 10, 0),
    ],
    "first-look": [
        ("ctr-by-position.png", f"{NB}/01_first_look_and_discovery.ipynb", 13, 0),
    ],
    "missing-data": [
        ("raw-distributions.png", f"{NB}/MissingDataStrategyEvaluation.ipynb", 13, 0),
        ("decline-raw.png", f"{NB}/MissingDataStrategyEvaluation.ipynb", 14, 0),
        ("decline-dropped.png", f"{NB}/MissingDataStrategyEvaluation.ipynb", 30, 0),
        ("correlation-dropped.png", f"{NB}/MissingDataStrategyEvaluation.ipynb", 33, 0),
        ("correlation-median.png", f"{NB}/MissingDataStrategyEvaluation.ipynb", 33, 1),
        ("imputer-correlations.png", f"{NB}/MissingDataStrategyEvaluation.ipynb", 35, 0),
        ("missing-flags.png", f"{NB}/MissingDataStrategyEvaluation.ipynb", 37, 0),
    ],
    "missing-data-warehouse": [
        ("mae-by-feature.png", "work/notebooks/FlyRank_DuckDB_Missing_Data_Strategy_Benchmark.ipynb", 22, 0),
        ("overall-error.png", "work/notebooks/FlyRank_DuckDB_Missing_Data_Strategy_Benchmark.ipynb", 30, 0),
    ],
    "full-release": [
        ("rf-importance.png", f"{NB}/03_working_with_the_full_release.ipynb", 19, 0),
        ("feature-correlation.png", f"{NB}/03_working_with_the_full_release.ipynb", 20, 0),
    ],
    "segmentation": [
        ("content-age.png", f"{NB}/Content_Segmentation_Unsupervised.ipynb", 13, 8),
        ("days-since-update.png", f"{NB}/Content_Segmentation_Unsupervised.ipynb", 13, 9),
        ("elbow.png", f"{NB}/Content_Segmentation_Unsupervised.ipynb", 18, 0),
        ("silhouette.png", f"{NB}/Content_Segmentation_Unsupervised.ipynb", 18, 1),
        ("dendrogram.png", f"{NB}/Content_Segmentation_Unsupervised.ipynb", 23, 0),
        ("k-distance.png", f"{NB}/Content_Segmentation_Unsupervised.ipynb", 26, 0),
        ("kmeans-pca.png", f"{NB}/Content_Segmentation_Unsupervised.ipynb", 31, 0),
        ("hierarchical-pca.png", f"{NB}/Content_Segmentation_Unsupervised.ipynb", 32, 0),
        ("dbscan-pca.png", f"{NB}/Content_Segmentation_Unsupervised.ipynb", 33, 0),
        ("trend-by-cluster.png", f"{NB}/Content_Segmentation_Unsupervised.ipynb", 41, 0),
    ],
    "segmentation-profiles": [
        ("kmeans-pca.png", f"{NB}/Content_Segmentation.ipynb", 36, 0),
        ("cluster-boxplots.png", f"{NB}/Content_Segmentation.ipynb", 42, 0),
        ("sessions-violin.png", f"{NB}/Content_Segmentation.ipynb", 44, 0),
        ("trend-by-cluster.png", f"{NB}/Content_Segmentation.ipynb", 53, 0),
    ],
    "pca": [
        ("explained-variance.png", f"{NB}/PCA_Dataset_Structure_DuckDB.ipynb", 15, 0),
        ("projection.png", f"{NB}/PCA_Dataset_Structure_DuckDB.ipynb", 17, 0),
    ],
    "anomaly-isolation-forest": [
        ("pca-anomalies.png", f"{NB}/Anomaly_Detection_Full_DuckDB_Release.ipynb", 23, 0),
    ],
    "anomaly-dbscan": [
        ("k-distance.png", f"{NB}/DBSCAN_Anomaly_Detection_DuckDB.ipynb", 12, 0),
        ("pca-noise.png", f"{NB}/DBSCAN_Anomaly_Detection_DuckDB.ipynb", 17, 0),
    ],
    "rec-eda": [
        ("priority-tiers.png", f"{REC}/EDA_on_Recommendation_Engine.ipynb", 7, 0),
        ("score-distribution.png", f"{REC}/EDA_on_Recommendation_Engine.ipynb", 9, 0),
        ("rank-distribution.png", f"{REC}/EDA_on_Recommendation_Engine.ipynb", 9, 1),
        ("ndcg-k5.png", f"{REC}/EDA_on_Recommendation_Engine.ipynb", 14, 0),
        ("ndcg-k10.png", f"{REC}/EDA_on_Recommendation_Engine.ipynb", 14, 1),
        ("feature-importance.png", f"{REC}/EDA_on_Recommendation_Engine.ipynb", 16, 0),
        ("gsc-availability.png", f"{REC}/EDA_on_Recommendation_Engine.ipynb", 18, 0),
        ("sampling-caps.png", f"{REC}/EDA_on_Recommendation_Engine.ipynb", 22, 0),
        ("score-by-tier.png", f"{REC}/EDA_on_Recommendation_Engine.ipynb", 35, 0),
        ("rank-vs-score.png", f"{REC}/EDA_on_Recommendation_Engine.ipynb", 35, 1),
        ("ndcg5-by-seed.png", f"{REC}/EDA_on_Recommendation_Engine.ipynb", 39, 0),
        ("ndcg10-by-seed.png", f"{REC}/EDA_on_Recommendation_Engine.ipynb", 39, 2),
        ("seed-method-ndcg10.png", f"{REC}/EDA_on_Recommendation_Engine.ipynb", 39, 3),
        ("spearman-heatmap.png", f"{REC}/EDA_on_Recommendation_Engine.ipynb", 41, 0),
        ("quality-scorecard.png", f"{REC}/EDA_on_Recommendation_Engine.ipynb", 45, 0),
        ("prev-impressions-by-tier.png", f"{REC}/EDA_on_Recommendation_Engine.ipynb", 48, 0),
        ("latest-impressions-by-tier.png", f"{REC}/EDA_on_Recommendation_Engine.ipynb", 48, 1),
        ("position-by-tier.png", f"{REC}/EDA_on_Recommendation_Engine.ipynb", 48, 2),
    ],
    "heuristic-baseline": [
        ("confusion-matrix.png", f"{NB}/HeuristicBaseline.ipynb", 17, 0),
        ("roc.png", f"{NB}/HeuristicBaseline.ipynb", 22, 0),
        ("rule-vs-forest.png", f"{NB}/HeuristicBaseline.ipynb", 26, 0),
        ("importance.png", f"{NB}/HeuristicBaseline.ipynb", 28, 0),
    ],
    "content-status": [
        ("model-comparison.png", f"{NB}/ContentStatusPrediction.ipynb", 19, 0),
        ("confusion-lightgbm.png", f"{NB}/ContentStatusPrediction.ipynb", 20, 0),
    ],
    "needs-refresh": [
        ("roc.png", f"{NB}/Binary_Classification_Needs_Refresh.ipynb", 18, 0),
        ("pr-curves.png", f"{NB}/Binary_Classification_Needs_Refresh.ipynb", 19, 0),
        ("confusion-xgboost.png", f"{NB}/Binary_Classification_Needs_Refresh.ipynb", 22, 0),
        ("threshold.png", f"{NB}/Binary_Classification_Needs_Refresh.ipynb", 25, 0),
        ("importance.png", f"{NB}/Binary_Classification_Needs_Refresh.ipynb", 30, 0),
    ],
    "regression": [
        ("importance.png", f"{NB}/Predict_30d_Impressions_with_Regression.ipynb", 23, 0),
        ("warehouse-linear.png", f"{NB}/Predict_30d_Impressions_with_Regression.ipynb", 38, 0),
        ("warehouse-log.png", f"{NB}/Predict_30d_Impressions_with_Regression.ipynb", 39, 0),
        ("intent-top10.png", f"{NB}/Predict_30d_Impressions_with_Regression.ipynb", 44, 0),
        ("tuned-linear.png", f"{NB}/Predict_30d_Impressions_with_Regression.ipynb", 51, 0),
    ],
    "shap": [
        ("roc.png", f"{NB}/Content_Decline_Explainability_SHAP_Aggregated.ipynb", 16, 0),
        ("pr.png", f"{NB}/Content_Decline_Explainability_SHAP_Aggregated.ipynb", 17, 0),
        ("permutation.png", f"{NB}/Content_Decline_Explainability_SHAP_Aggregated.ipynb", 22, 0),
        ("beeswarm.png", f"{NB}/Content_Decline_Explainability_SHAP_Aggregated.ipynb", 25, 0),
        ("aggregated.png", f"{NB}/Content_Decline_Explainability_SHAP_Aggregated.ipynb", 30, 0),
        ("pdp-prev30.png", f"{NB}/Content_Decline_Explainability_SHAP_Aggregated.ipynb", 33, 0),
        ("pdp-position.png", f"{NB}/Content_Decline_Explainability_SHAP_Aggregated.ipynb", 33, 3),
        ("pdp-age.png", f"{NB}/Content_Decline_Explainability_SHAP_Aggregated.ipynb", 33, 5),
        ("local-highest.png", f"{NB}/Content_Decline_Explainability_SHAP_Aggregated.ipynb", 38, 0),
        ("local-false-positive.png", f"{NB}/Content_Decline_Explainability_SHAP_Aggregated.ipynb", 40, 0),
        ("local-false-negative.png", f"{NB}/Content_Decline_Explainability_SHAP_Aggregated.ipynb", 42, 0),
    ],
    "rec-v1": [
        ("tiers.png", f"{NB}/FlyRank_Content_Refresh_Recommendation_Engine.ipynb", 19, 0),
        ("tier-scatter.png", f"{NB}/FlyRank_Content_Refresh_Recommendation_Engine.ipynb", 19, 1),
    ],
    "rec-stage1": [
        ("tiers.png", f"{REC}/FlyRank_Content_Refresh_Recommendation_Engine_Stage1_Validation.ipynb", 27, 0),
        ("tier-scatter.png", f"{REC}/FlyRank_Content_Refresh_Recommendation_Engine_Stage1_Validation.ipynb", 27, 1),
    ],
    "rec-stage2": [
        ("ndcg.png", f"{REC}/FlyRank_Content_Refresh_Recommendation_Engine_Stage2.ipynb", 29, 0),
        ("importance.png", f"{REC}/FlyRank_Content_Refresh_Recommendation_Engine_Stage2.ipynb", 35, 0),
    ],
    "rec-stage3": [
        ("ndcg.png", f"{REC}/FlyRank_Content_Refresh_Recommendation_Engine_Stage3_Business_Impact_Tracking.ipynb", 30, 0),
    ],
    "rec-stage4": [
        ("summary.png", f"{REC}/FlyRank_Content_Refresh_Recommendation_Engine_Stage4_Production_Readiness_and_Monitoring.ipynb", 76, 0),
    ],
    "rec-final-integrated": [
        ("summary.png", f"{REC}/FlyRank_Content_Refresh_Recommendation_Engine_Final_Integrated_Draft.ipynb", 76, 0),
    ],
    "rec-final-gated": [
        ("ndcg.png", f"{REC}/FlyRank_Content_Refresh_Recommendation_Engine_Final_Validation_Gated.ipynb", 34, 0),
        ("importance.png", f"{REC}/FlyRank_Content_Refresh_Recommendation_Engine_Final_Validation_Gated.ipynb", 40, 0),
        ("summary.png", f"{REC}/FlyRank_Content_Refresh_Recommendation_Engine_Final_Validation_Gated.ipynb", 84, 0),
    ],
    "ml-08-capstone-modeling": [
        ("importance.png", "work/notebooks/w08_capstone_modeling.ipynb", 11, 0),
    ],
    "milestone-5": [
        ("review-tiers.png", "work/notebooks/milestone_5_action_playbook.ipynb", 12, 0),
        ("reasons-logistic.png", "work/notebooks/milestone_5_action_playbook.ipynb", 13, 0),
        ("score-distributions.png", "work/notebooks/milestone_5_action_playbook.ipynb", 15, 0),
        ("reasons-forest.png", "work/notebooks/milestone_5_action_playbook.ipynb", 18, 0),
        ("reason-correlation.png", "work/notebooks/milestone_5_action_playbook.ipynb", 21, 0),
    ],
    "milestone-6": [
        ("average-precision.png", "work/notebooks/milestone_6_model_performance_analysis.ipynb", 10, 0),
    ],
}


def images_in_cell(cell):
    for output in cell.get("outputs", []):
        data = output.get("data", {})
        if "image/png" in data:
            yield data["image/png"]


def main():
    written = 0
    for slug, figures in FIGURES.items():
        for name, notebook, cell_index, nth in figures:
            cells = json.loads((ROOT / notebook).read_text())["cells"]
            images = list(images_in_cell(cells[cell_index]))
            if nth >= len(images):
                raise SystemExit(f"{notebook} cell {cell_index} has no image #{nth}")
            target = OUT / slug / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(base64.b64decode(images[nth]))
            written += 1
    print(f"Wrote {written} figures to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
