import pandas as pd
import numpy as np
from linnaeus import classification

RAW_DATA_DIR = "./raw_data"
PROCESSED_DATA_DIR = "./processed_data"


ADDITIONAL_COUNTRIES = pd.DataFrame(
    [
        [
            251,
            "LIE",
            "country",
            "Liechtenstein",
            "Liechtenstein",
            "LI",
            "4",
            "Liechtenstein",
            False,
            False,
            False,
            False,
            False,
        ],
        [
            252,
            "MCO",
            "country",
            "Monaco",
            "Monaco",
            "MC",
            "4",
            "Monaco",
            False,
            False,
            False,
            False,
            False,
        ],
    ],
    columns=[
        "location_id",
        "code",
        "level",
        "name_en",
        "name_short_en",
        "iso2",
        "parent_id",
        "name",
        "is_trusted",
        "in_rankings",
        "reported_serv",
        "reported_serv_recent",
        "former_country",
    ],
).set_index("location_id")


if __name__ == "__main__":
    nace = classification.load("industry/NACE/Albania/out/nace_industries.csv").table
    alb_countries = classification.load(
        "location/International/Atlas/out/locations_international_atlas.csv"
    ).table

    # Map countries from FDI set to Location IDs
    alb_countries = pd.concat([alb_countries, ADDITIONAL_COUNTRIES])
    alb_countries = alb_countries.reset_index().rename(columns={"index": "location_id"})
    alb_countries = alb_countries[
        [
            "location_id",
            "code",
            "level",
            "name_en",
            "name_short_en",
            "iso2",
            "parent_id",
            "name",
            "is_trusted",
            "in_rankings",
            "reported_serv",
            "reported_serv_recent",
            "former_country",
        ]
    ]
    alb_countries.to_csv(f"{PROCESSED_DATA_DIR}/country.csv", index=False)

    # Process NACE to table
    nace = nace.reset_index().rename(columns={"index": "nace_id"})
    nace.to_csv(f"{PROCESSED_DATA_DIR}/nace_industry.csv", index=False)

    # Ingest script table
    script = pd.read_csv(f"{RAW_DATA_DIR}/albania_script.csv")
    script.to_csv(f"{PROCESSED_DATA_DIR}/script.csv", index=False)

    # Ingest Viability and Attractiveness Factors
    nace_group = nace[nace.level == "group"]
    nace_group["code"] = nace_group.code.astype(float)
    nace_group["code_int"] = (
        nace_group.code.astype(str).str.replace(".", "").astype(int)
    )

    factors = pd.read_csv(f"{RAW_DATA_DIR}/combined_factors_may8.csv")
    factors = factors.merge(
        nace_group, left_on="description", right_on="name", how="left"
    )[
        [
            "nace_id",
            "rca",
            "v_rca",
            "v_dist",
            "v_fdipeers",
            "v_contracts",
            "v_elect",
            "avg_viability",
            "a_youth",
            "a_wage",
            "a_fdiworld",
            "a_export",
            "avg_attractiveness",
            "v_text",
            "a_text",
            "strategy",
            "rca",
            "rca_text1",
            "rca_text2",
        ]
    ]
    factors = factors.loc[:, ~factors.columns.duplicated()]
    factors.to_csv(f"{PROCESSED_DATA_DIR}/factors.csv", index=False)

    # Industry Now
    industry_now_file = f"{RAW_DATA_DIR}/IndustryNow_april20.xls"
    industry_now_drop_cols = [
        "nace",
        "description",
        "level",
        "code",
        "code_int",
        "name",
        "parent_id",
    ]

    industry_now_tables = {
        "industry_now_location": "1_location",
        "industry_now_schooling": "2_schooling",
        "industry_now_occupation": "3_occupations",
        "industry_now_wage": "4_wages_histogram",
        "industry_now_nearest_industry": "5_nearest_industries",
    }

    industry_now_data = {}

    for table, sheet in industry_now_tables.items():
        df = pd.read_excel(industry_now_file, sheet)
        df.columns = [x.lower() for x in df.columns]
        df = df.merge(nace_group, left_on="nace", right_on="code_int", how="left").drop(
            columns=industry_now_drop_cols
        )
        industry_now_data[table] = df
        if table != "industry_now_nearest_industry":
            df.to_csv(f"{PROCESSED_DATA_DIR}/{table}.csv", index=False)

    industry_now_nearest_industry = industry_now_data["industry_now_nearest_industry"]
    industry_now_nearest_industry = (
        pd.wide_to_long(
            industry_now_nearest_industry,
            ["nearby_", "description_", "rca_"],
            i="nace_id",
            j="place",
        )
        .reset_index()
        .rename(
            columns={
                "nearby_": "neighbor_code",
                "description_": "neighbor_name",
                "rca_": "neighbor_rca_gte1",
            }
        )
    )

    industry_now_nearest_industry = (
        industry_now_nearest_industry.merge(
            nace_group,
            left_on="neighbor_code",
            right_on="code_int",
            how="left",
            suffixes=("", "_neighbor"),
        )
        .drop(
            columns=["neighbor_code", "neighbor_name", "level", "parent_id", "code_int"]
        )
        .rename(
            columns={
                "nace_id_neighbor": "neighbor_nace_id",
                "code": "neighbor_code",
                "name": "neighbor_name",
            }
        )
    )

    industry_now_nearest_industry.neighbor_rca_gte1 = industry_now_nearest_industry.neighbor_rca_gte1.apply(
        lambda x: {"No": False, "Yes": True, np.NaN: np.NaN}[x]
    )

    industry_now_nearest_industry.to_csv(
        f"{PROCESSED_DATA_DIR}/industry_now_nearest_industry.csv", index=False
    )
