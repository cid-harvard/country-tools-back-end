import pandas as pd
from os import path

RAW_DATA_DIR = "./raw_data"
PROCESSED_DATA_DIR = "./processed_data"

if __name__ == "__main__":
    ATTRACTIVENESS_COLS = [
        "a_relative_demand",
        "a_resiliency",
        "a_employment_groups_interest",
        "a_fdi",
        "a_export_propensity",
    ]
    FEASIBILITY_COLS = [
        "f_port_propensity",
        "f_existing_presence",
        "f_remoteness",
        "f_scarce_factors",
        "f_input_availability",
    ]

    # Load A/V factor files ------------------------------------------------------------
    ## HS 4-digit
    hs_df = pd.read_csv(
        path.join(RAW_DATA_DIR, "HS4_universe_nam_investment_tool.csv"),
        dtype={"hs4": str},
    )

    ## NAICS 6-digit
    naics_df = pd.read_csv(
        path.join(RAW_DATA_DIR, "NAICS_universe_nam_investment_tool.csv"),
        dtype={"naics": str},
    )

    # Classifications ------------------------------------------------------------------
    ## HS 4-digit Classification -------------------------------------------------------
    hs_classification = pd.read_csv(
        path.join(RAW_DATA_DIR, "hs_classification.csv")
    ).rename(columns={"id": "hs_id", "name_en": "name"})
    hs_classification = hs_classification[hs_classification.level == "4digit"]
    hs_classification = hs_classification[
        ["hs_id", "name", "code", "level", "parent_id"]
    ]

    ### Merge data to determine flags
    hs_classification = hs_classification.merge(
        hs_df[["hs4", "complexity_report"]], left_on="code", right_on="hs4", how="left"
    )
    hs_classification["in_tool"] = hs_classification.hs4.notna()
    hs_classification["complexity_report"] = hs_classification.complexity_report.astype(
        bool
    ).fillna(False)
    hs_classification = hs_classification.drop(columns="hs4").drop_duplicates()

    ## NAICS 6-digit Classification ----------------------------------------------------
    naics_classification = pd.read_csv(
        path.join(RAW_DATA_DIR, "naics_classification.csv")
    )
    naics_classification = naics_classification[naics_classification.level == 6]
    naics_classification = naics_classification[
        ["naics_id", "name", "code", "level", "parent_id"]
    ]

    ### Merge data to determine flags
    naics_classification = naics_classification.merge(
        naics_df[["naics", "complexity_report"]],
        left_on="code",
        right_on="naics",
        how="left",
    )
    naics_classification["in_tool"] = naics_classification.naics.notna()
    naics_classification[
        "complexity_report"
    ] = naics_classification.complexity_report.astype(bool).fillna(False)
    naics_classification = naics_classification.drop(columns="naics").drop_duplicates()

    # Format Attractiveness/Viability factors data -------------------------------------
    ## HS 4-digit ----------------------------------------------------------------------
    hs_df = hs_df.merge(
        hs_classification[["code", "hs_id"]], left_on="hs4", right_on="code"
    )[["hs_id", *ATTRACTIVENESS_COLS, *FEASIBILITY_COLS]]
    hs_df["attractiveness"] = hs_df[ATTRACTIVENESS_COLS].mean(axis=1)
    hs_df["feasibility"] = hs_df[FEASIBILITY_COLS].mean(axis=1)

    ## NAICS 6-digit -------------------------------------------------------------------
    naics_df = naics_df.merge(
        naics_classification[["code", "naics_id"]], left_on="naics", right_on="code"
    )[["naics_id", *ATTRACTIVENESS_COLS, *FEASIBILITY_COLS]]
    naics_df["attractiveness"] = naics_df[ATTRACTIVENESS_COLS].mean(axis=1)
    naics_df["feasibility"] = naics_df[FEASIBILITY_COLS].mean(axis=1)

    # Save files -----------------------------------------------------------------------
    hs_classification.to_csv(
        path.join(PROCESSED_DATA_DIR, "hs_classification.csv"), index=False
    )
    naics_classification.to_csv(
        path.join(PROCESSED_DATA_DIR, "naics_classification.csv"), index=False
    )
    hs_df.to_csv(path.join(PROCESSED_DATA_DIR, "hs_factors.csv"), index=False)
    naics_df.to_csv(path.join(PROCESSED_DATA_DIR, "naics_factors.csv"), index=False)
