"""FlyRank starter-CSV audit helper.

The primary warehouse implementation is ``milestone_1_warehouse_audit.ipynb``.
This helper is retained for auditing a dataframe already shaped like the starter
CSV contract; it does not connect to Hugging Face or define the warehouse windows.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import pandas as pd

PAGE_ID = "content_id"
GROUP_ID = "client_id"
TARGET_SOURCE = "trend_direction"
TARGET = "is_declining_label"
BASE_FEATURES = [
    "days_since_last_update",
    "content_age_days",
    "impressions_90d",
    "avg_position",
    "ctr",
]
GSC_FIELDS = ["impressions_90d", "avg_position", "ctr"]
CONTEXT_FIELDS = [PAGE_ID, GROUP_ID, "content_type"]
EXCLUDED_PREDICTORS = [TARGET_SOURCE, "trend_pct", TARGET, PAGE_ID, GROUP_ID]
REQUIRED_COLUMNS = [PAGE_ID, GROUP_ID, TARGET_SOURCE, *BASE_FEATURES]
CSV_PROTOTYPE_CANDIDATES = [
    "days_since_last_update",
    "content_age_days",
    "content_type",
    "main_intent",
    "competition_level",
    "word_count",
    "char_count",
]


def run_audit(
    raw_df: pd.DataFrame,
    output_dir: Path,
    *,
    source_name: str = "existing DuckDB + Hugging Face result",
    temporal_contract_confirmed: bool = False,
    features_as_of: str | None = None,
    label_window_start: str | None = None,
    label_window_end: str | None = None,
) -> dict[str, Any]:
    """Audit source rows, write reproducible outputs, and return the summary.

    Set ``temporal_contract_confirmed`` only after verifying source metadata and
    recording feature cutoff and label-window bounds. Candidate fields must be
    observed no later than the beginning of the label window.
    """
    missing_columns = sorted(set(REQUIRED_COLUMNS) - set(raw_df.columns))
    if missing_columns:
        raise ValueError(f"Missing contract columns: {missing_columns}")

    if temporal_contract_confirmed:
        if not (features_as_of and label_window_start and label_window_end):
            raise ValueError("Confirmed temporal contract requires all three time bounds.")
        feature_time = pd.Timestamp(features_as_of)
        label_start = pd.Timestamp(label_window_start)
        label_end = pd.Timestamp(label_window_end)
        if label_start >= label_end or feature_time > label_start:
            raise ValueError(
                "Invalid temporal order: features must be observed at/before label-window start."
            )

    df = raw_df.copy()
    df[TARGET_SOURCE] = df[TARGET_SOURCE].astype("string").str.strip().str.lower()
    df[TARGET] = df[TARGET_SOURCE].map(
        {"down": 1, "new": 0, "up": 0, "flat": 0, "stable": 0}
    ).astype("Int64")
    for field in BASE_FEATURES:
        df[field] = pd.to_numeric(df[field], errors="coerce")

    audit = pd.DataFrame(index=df.index)
    audit[PAGE_ID] = df[PAGE_ID]
    audit[GROUP_ID] = df[GROUP_ID]
    audit["label_valid"] = df[TARGET].notna()
    audit["ids_valid"] = df[PAGE_ID].notna() & df[GROUP_ID].notna()
    audit["page_id_unique"] = ~df[PAGE_ID].duplicated(keep=False)
    # The starter contract defines avg_position == 0 as "no position data".
    # Treat it as unavailable even though the stored value is non-null.
    audit["gsc_available"] = df[GSC_FIELDS].notna().all(axis=1) & df["avg_position"].gt(0)
    audit["temporal_contract_confirmed"] = bool(temporal_contract_confirmed)
    # Fast CSV prototyping is about code, missingness, and a client-held-out
    # baseline. It does not certify temporal validity or early-warning ability.
    audit["eligible_for_csv_prototyping"] = (
        audit["label_valid"] & audit["ids_valid"] & audit["page_id_unique"]
    )
    audit["eligible_for_primary_model"] = (
        audit["label_valid"]
        & audit["ids_valid"]
        & audit["page_id_unique"]
        & audit["gsc_available"]
        & audit["temporal_contract_confirmed"]
    )

    def exclusion_reasons(row: pd.Series) -> str:
        checks = [
            ("invalid_or_missing_label", row["label_valid"]),
            ("missing_page_or_client_id", row["ids_valid"]),
            ("duplicate_content_id", row["page_id_unique"]),
            ("missing_one_or_more_gsc_fields", row["gsc_available"]),
            ("temporal_provenance_unverified", row["temporal_contract_confirmed"]),
        ]
        return ";".join(name for name, passed in checks if not passed)

    audit["exclusion_reasons"] = audit.apply(exclusion_reasons, axis=1)
    missingness = pd.DataFrame(
        {
            "field": df.columns,
            "dtype": [str(df[c].dtype) for c in df.columns],
            "missing_count": [int(df[c].isna().sum()) for c in df.columns],
            "missing_rate": [float(df[c].isna().mean()) for c in df.columns],
            "distinct_count": [int(df[c].nunique(dropna=True)) for c in df.columns],
        }
    )
    prototype_features = [c for c in CSV_PROTOTYPE_CANDIDATES if c in df.columns]
    if not prototype_features:
        raise ValueError("No CSV prototype features are present in the source data.")
    missingness_by_content_type = (
        df.groupby("content_type", dropna=False)[prototype_features]
        .agg(lambda col: col.isna().mean())
        .rename_axis("content_type")
        .reset_index()
    )
    gsc_by_client = df.groupby(GROUP_ID, dropna=False)[GSC_FIELDS].agg(["count", "size"])
    gsc_by_client.columns = [f"{field}_{stat}" for field, stat in gsc_by_client.columns]
    for field in GSC_FIELDS:
        gsc_by_client[f"{field}_available_rate"] = (
            gsc_by_client[f"{field}_count"] / gsc_by_client[f"{field}_size"]
        )

    summary = {
        "source": source_name,
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "unique_content_ids": int(df[PAGE_ID].nunique(dropna=True)),
        "unique_clients": int(df[GROUP_ID].nunique(dropna=True)),
        "duplicate_content_id_rows": int(df[PAGE_ID].duplicated(keep=False).sum()),
        "target_counts": {
            str(k): int(v) for k, v in df[TARGET].value_counts(dropna=False).items()
        },
        "gsc_complete_rows": int(audit["gsc_available"].sum()),
        "eligible_rows": int(audit["eligible_for_primary_model"].sum()),
        "csv_prototype_rows": int(audit["eligible_for_csv_prototyping"].sum()),
        "csv_prototype_feature_columns": prototype_features,
        "temporal_contract_confirmed": bool(temporal_contract_confirmed),
    }

    contract = {
        "modelling_unit": "one unique content_id page within client_id",
        "target": TARGET,
        "target_rule": "1 if normalized trend_direction is 'down'; 0 for known values new/up/flat/stable; otherwise unlabeled",
        "candidate_features": BASE_FEATURES,
        "engineered_feature": "staleness_pos_interaction = days_since_last_update * avg_position; only after temporal checks pass",
        "gsc_fields": GSC_FIELDS,
        "context_only": CONTEXT_FIELDS,
        "excluded_predictors": EXCLUDED_PREDICTORS,
        "missing_gsc_policy": "retain in audit; do not zero-impute; exclude from primary model when any required GSC value is missing",
        "freshness_missing_policy": "report missingness; impute only inside training folds and add missingness indicators",
        "eligibility": "valid target, non-null page/client IDs, unique content_id, complete required GSC fields, and verified temporal contract",
        "temporal_contract_confirmed": bool(temporal_contract_confirmed),
        "features_as_of": features_as_of,
        "label_window_start": label_window_start,
        "label_window_end": label_window_end,
        "temporal_status": (
            "verified"
            if temporal_contract_confirmed
            else "UNVERIFIED: do not certify candidate features as pre-outcome"
        ),
        "csv_development_mode": {
            "purpose": "fast pipeline, missingness, and client-holdout prototype work only",
            "eligible_rows": int(audit["eligible_for_csv_prototyping"].sum()),
            "features": prototype_features,
            "not_supported": "temporal validation or future early-warning claims; starter CSV lacks the older GSC feature window needed for the final temporal contract",
        },
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    missingness.to_csv(output_dir / "field_missingness.csv", index=False)
    missingness_by_content_type.to_csv(
        output_dir / "field_missingness_by_content_type.csv", index=False
    )
    gsc_by_client.to_csv(output_dir / "gsc_availability_by_client.csv")
    audit.to_csv(output_dir / "row_eligibility.csv", index=False)
    csv_prototype = df.loc[
        audit["eligible_for_csv_prototyping"],
        [PAGE_ID, GROUP_ID, TARGET, *prototype_features],
    ].copy()
    csv_prototype.to_csv(output_dir / "csv_prototype_dataset.csv", index=False)
    (output_dir / "audit_summary.json").write_text(
        json.dumps(summary, indent=2, default=str) + "\n", encoding="utf-8"
    )
    (output_dir / "data_contract.json").write_text(
        json.dumps(contract, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2, default=str))
    print(f"Audit outputs written to {output_dir.resolve()}")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--csv",
        type=Path,
        default=Path("data/raw/content_refresh_anonymized.csv"),
        help="Local starter CSV matching the content_id/trend_direction contract.",
    )
    parser.add_argument("--output-dir", type=Path, default=Path("work/outputs/milestone_1"))
    args = parser.parse_args()
    if not args.csv.exists():
        raise FileNotFoundError(
            f"{args.csv} not found. Use milestone_1_warehouse_audit.ipynb for the "
            "DuckDB/HF workflow, or provide a local starter CSV."
        )
    run_audit(pd.read_csv(args.csv), args.output_dir, source_name=str(args.csv))


if __name__ == "__main__":
    main()
