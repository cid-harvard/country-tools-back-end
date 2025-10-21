import json
from os import path
import pandas as pd
import numpy as np

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
        path.join(RAW_DATA_DIR, "HS4", "HS4_universe_nam_investment_tool.csv"),
        dtype={"hs4": str},
    )
    hs_df.hs4 = hs_df.hs4.str.pad(4, fillchar="0")

    ## NAICS 6-digit
    naics_df = pd.read_csv(
        path.join(RAW_DATA_DIR, "HS4", "NAICS_universe_nam_investment_tool.csv"),
        dtype={"naics": str},
    )

    # Classifications ------------------------------------------------------------------
    ## HS 4-digit Classification -------------------------------------------------------
    hs_classification = pd.read_csv(
        path.join(RAW_DATA_DIR, "classifications", "hs_classification.csv")
    ).rename(columns={"id": "hs_id", "name_short_en": "name"})
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
        path.join(RAW_DATA_DIR, "classifications", "naics_classification.csv")
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

    hs_rca = (
        pd.read_csv(path.join(RAW_DATA_DIR, "rca_hs.csv"))
        .rename(columns={"product_id": "hs_id", "export_rca": "rca"})[["hs_id", "rca"]]
        .drop_duplicates()
    )

    hs_df = hs_df.merge(hs_rca, on="hs_id", how="left")

    ## NAICS 6-digit -------------------------------------------------------------------
    naics_df = naics_df.merge(
        naics_classification[["code", "naics_id"]], left_on="naics", right_on="code"
    )[["naics_id", *ATTRACTIVENESS_COLS, *FEASIBILITY_COLS]]
    naics_df["attractiveness"] = naics_df[ATTRACTIVENESS_COLS].mean(axis=1)
    naics_df["feasibility"] = naics_df[FEASIBILITY_COLS].mean(axis=1)

    naics_rca = (
        pd.read_csv(
            path.join(RAW_DATA_DIR, "HS4", "rca_naics.csv"), dtype={"naics": str}
        )
        .rename(columns={"rca_mean": "rca"})[["naics", "rca"]]
        .merge(
            naics_classification[["code", "naics_id"]], left_on="naics", right_on="code"
        )
        .drop(columns=["code", "naics"])
        .drop_duplicates()
    )

    naics_df = naics_df.merge(naics_rca, on="naics_id", how="left")

    # Merge Industry Now product-level factors -----------------------------------------
    ## HS 4-digit ----------------------------------------------------------------------
    hs_eg = (
        pd.read_excel(
            path.join(
                RAW_DATA_DIR,
                "HS4",
                "Industry Characteristics - Visualization Data",
                "Employment Groups of Interest",
                "factor_data_hs4-employment_groups.xlsx",
            ),
            dtype={"hs4": str},
        )
        .merge(hs_classification[["code", "hs_id"]], left_on="hs4", right_on="code")
        .drop(columns=["code", "hs4"])
    )

    hs_df = hs_df.merge(hs_eg, on="hs_id", how="left")

    ## NAICS 6-digit -------------------------------------------------------------------
    naics_eg = (
        pd.read_csv(
            path.join(
                RAW_DATA_DIR,
                "HS4",
                "Industry Characteristics - Visualization Data",
                "Employment Groups of Interest",
                "factor_data_naics-employment_groups.csv",
            ),
            dtype={"naics": str},
        )
        .merge(
            naics_classification[["code", "naics_id"]], left_on="naics", right_on="code"
        )
        .drop(columns=["code", "naics"])
    )

    naics_df = naics_df.merge(naics_eg, on="naics_id", how="left")

    # Format country relative demand per product/industry ---------------------------------------
    ## HS 4-digit ----------------------------------------------------------------------
    hs_relative_demand = (
        pd.read_excel(
            path.join(
                RAW_DATA_DIR,
                "HS4",
                "Industry Characteristics - Visualization Data",
                "Relative Demand",
                "factor_data_hs4-relative_demand_rounded.xlsx",
            ),
            dtype={"hs4": str},
        )
        .merge(hs_classification[["code", "hs_id"]], left_on="hs4", right_on="code")
        .drop(columns=["code", "hs4"])
    )

    ## NAICS 6-digit -------------------------------------------------------------------
    naics_relative_demand = (
        pd.read_csv(
            path.join(
                RAW_DATA_DIR,
                "HS4",
                "Industry Characteristics - Visualization Data",
                "Relative Demand",
                "factor_data_naics-relative_demand_rounded.csv",
            ),
            dtype={"naics": str},
        )
        .merge(
            naics_classification[["code", "naics_id"]], left_on="naics", right_on="code"
        )
        .drop(columns=["code", "naics"])
    )

    # Format occupational data ---------------------------------------------------------
    ## HS 4-digit ----------------------------------------------------------------------
    hs_occupation = (
        pd.read_excel(
            path.join(
                RAW_DATA_DIR,
                "HS4",
                "Industry Characteristics - Visualization Data",
                "Input Availability - Occupations",
                "LIST_factor_data_hs4-top_occupations_withshares.xlsx",
            ),
            dtype={"hs4": str},
        )
        .merge(hs_classification[["code", "hs_id"]], left_on="hs4", right_on="code")
        .drop(columns=["code", "hs4"])
    )
    hs_occupation["is_available"] = hs_occupation.avail_rank.notna()
    hs_occupation["rank"] = hs_occupation.avail_rank.combine_first(
        hs_occupation.missing_rank
    )
    hs_occupation["pct_share"] = hs_occupation.avail_pct_share.combine_first(
        hs_occupation.missing_pct_share
    )
    hs_occupation = hs_occupation.drop(
        columns=["avail_rank", "missing_rank", "avail_pct_share", "missing_pct_share"]
    )

    ## NAICS 6-digit -------------------------------------------------------------------
    naics_occupation = (
        pd.read_csv(
            path.join(
                RAW_DATA_DIR,
                "HS4",
                "Industry Characteristics - Visualization Data",
                "Input Availability - Occupations",
                "LIST_factor_data_naics-top_occupations_withshares.csv",
            ),
            dtype={"naics": str},
        )
        .merge(
            naics_classification[["code", "naics_id"]], left_on="naics", right_on="code"
        )
        .drop(columns=["code", "naics"])
    )
    naics_occupation["is_available"] = naics_occupation.avail_rank.notna()
    naics_occupation["rank"] = naics_occupation.avail_rank.combine_first(
        naics_occupation.missing_rank
    )
    naics_occupation["pct_share"] = naics_occupation.avail_pct_share.combine_first(
        naics_occupation.missing_pct_share
    )
    naics_occupation = naics_occupation.drop(
        columns=["avail_rank", "missing_rank", "avail_pct_share", "missing_pct_share"]
    )

    # Format Proximity data ------------------------------------------------------------
    ## HS 4-digit ----------------------------------------------------------------------
    hs_prox = pd.read_csv(
        path.join(RAW_DATA_DIR, "hs92_proximities.csv"),
        dtype={"commoditycode_1": str, "commoditycode_2": str},
    )

    hs_prox = (
        hs_prox.merge(
            hs_classification[["code", "hs_id"]],
            left_on="commoditycode_2",
            right_on="code",
        )
        .drop(columns=["code", "commoditycode_2"])
        .rename(columns={"hs_id": "partner_id"})
        .merge(
            hs_classification[["code", "hs_id"]],
            left_on="commoditycode_1",
            right_on="code",
        )
        .drop(columns=["code", "commoditycode_1"])
    )

    ### Filter same ID-partner pairs
    hs_prox = hs_prox[hs_prox.hs_id != hs_prox.partner_id]

    ### Create rank variable (higher proximity is better)
    hs_prox["rank"] = hs_prox.groupby("hs_id").proximity.rank(
        ascending=False, method="max"
    )

    ### Filter to limit each product to no more than 10 partners
    hs_prox = hs_prox[hs_prox["rank"] <= 10]

    ## NAICS 6-digit -------------------------------------------------------------------
    with open(
        path.join(RAW_DATA_DIR, "NAICS-industry-industry-proximity-top-values.json"),
        "r",
    ) as f:
        j = json.load(f)

    naics_prox_data = []

    for node in j.get("nodes"):
        src = node.get("id")
        for edge in node.get("edges"):
            edge["src"] = src
            naics_prox_data.append(edge)

    naics_prox = pd.DataFrame(naics_prox_data).rename(
        columns={"src": "naics_id", "trg": "partner_id"}
    )

    ### Filter same ID-partner pairs
    naics_prox = naics_prox[naics_prox.naics_id != naics_prox.partner_id]

    ### Create rank variable (higher proximity is better)
    naics_prox["rank"] = naics_prox.groupby("naics_id").proximity.rank(
        ascending=False, method="max"
    )

    ### Filter to limit each product to no more than 10 partners
    naics_prox = naics_prox[naics_prox["rank"] <= 10]

    # Threshold Values -----------------------------------------------------------------

    employment_avgshares = pd.read_excel(
        path.join(
            RAW_DATA_DIR,
            "HS4",
            "Industry Characteristics - Visualization Data",
            "Employment Groups of Interest",
            "factor_data_naics-employment_groups_econ_avgshares.xlsx",
        )
    )
    employment_avgshares = employment_avgshares.set_index("interest_group").T

    thresh = {
        "hs_attractiveness_avg": hs_df.attractiveness.mean(),
        "hs_feasibility_avg": hs_df.feasibility.mean(),
        "naics_attractiveness_avg": naics_df.attractiveness.mean(),
        "naics_feasibility_avg": naics_df.feasibility.mean(),
        "hs_attractiveness_med": hs_df.attractiveness.median(),
        "hs_feasibility_med": hs_df.feasibility.median(),
        "naics_attractiveness_med": naics_df.attractiveness.median(),
        "naics_feasibility_med": naics_df.feasibility.median(),
        "employment_female_avg": employment_avgshares.female[0] / 100.0,
        "employment_youth_avg": employment_avgshares.youth[0] / 100.0,
        "employment_lskill_avg": employment_avgshares.lskill[0] / 100.0,
    }

    thresh = pd.DataFrame.from_dict(thresh, orient="index").reset_index()
    thresh.columns = ("key", "value")

    # Save files -----------------------------------------------------------------------
    hs_classification.to_csv(
        path.join(PROCESSED_DATA_DIR, "hs_classification.csv"), index=False
    )
    naics_classification.to_csv(
        path.join(PROCESSED_DATA_DIR, "naics_classification.csv"), index=False
    )
    hs_df.drop_duplicates().to_csv(
        path.join(PROCESSED_DATA_DIR, "hs_factors.csv"), index=False
    )
    naics_df.drop_duplicates().to_csv(
        path.join(PROCESSED_DATA_DIR, "naics_factors.csv"), index=False
    )

    hs_relative_demand.to_csv(
        path.join(PROCESSED_DATA_DIR, "hs_relative_demand.csv"), index=False
    )
    naics_relative_demand.to_csv(
        path.join(PROCESSED_DATA_DIR, "naics_relative_demand.csv"), index=False
    )

    hs_occupation.to_csv(
        path.join(PROCESSED_DATA_DIR, "hs_occupation.csv"), index=False
    )
    naics_occupation.to_csv(
        path.join(PROCESSED_DATA_DIR, "naics_occupation.csv"), index=False
    )

    hs_prox.to_csv(path.join(PROCESSED_DATA_DIR, "hs_proximity.csv"), index=False)
    naics_prox.to_csv(path.join(PROCESSED_DATA_DIR, "naics_proximity.csv"), index=False)

    thresh.to_csv(path.join(PROCESSED_DATA_DIR, "threshold.csv"), index=False)
