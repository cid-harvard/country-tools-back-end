import pandas as pd
import numpy as np
from linnaeus import classification

RAW_DATA_DIR = "./raw_data"
PROCESSED_DATA_DIR = "./processed_data"

MANUAL_MAPPINGS = {
    "Russia": 186,
    "United States": 231,
    "UAE": 7,
    "Monaco": None,
    "Syria": 212,
    "Bosnia-Herzegovina": 26,
    "Cote d Ivoire": 44,
    "Macau": 133,
    "Liechtenstein": None,
    "Brunei": 34,
    "Trinidad & Tobago": 222,
    "Democratic Republic of Congo": 46,
    "Republic of the Congo": 47,
}

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


def fdi_countries_to_loc_class(fdi, loc):
    fdi_countries = pd.DataFrame(fdi.source_country.drop_duplicates())

    loc = loc[["code", "name_en", "name_short_en"]].reset_index()
    loc = loc.rename(columns={"index": "location_id"})

    fdi_countries = fdi_countries.merge(
        loc, left_on="source_country", right_on="name_en", how="left"
    ).merge(
        loc,
        left_on="source_country",
        right_on="name_short_en",
        how="left",
        suffixes=("_name", "_name_short"),
    )

    manual_countries = pd.DataFrame(
        pd.Series(MANUAL_MAPPINGS, index=MANUAL_MAPPINGS.keys())
    ).reset_index()
    manual_countries.columns = ["name", "location_id"]

    fdi_countries = fdi_countries.merge(
        manual_countries, left_on="source_country", right_on="name", how="left"
    )

    fdi_countries["location_id"] = (
        fdi_countries["location_id"]
        .fillna(fdi_countries["location_id_name"])
        .fillna(fdi_countries["location_id_name_short"])
    )

    return fdi_countries[["source_country", "location_id"]]


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

    # Ingest FDI data
    fdi = pd.read_csv(f"{RAW_DATA_DIR}/fDiMarkets_nace_companies_v2.csv")
    fdi.columns = [
        "code",
        "nace_digits",
        "name",
        "parent_company",
        "source_country",
        "source_city",
        "capex_world",
        "capex_europe",
        "capex_balkans",
        "projects_world",
        "projects_europe",
        "projects_balkans",
        "avg_capex",
        "avg_jobs",
    ]

    fdi_countries = fdi_countries_to_loc_class(fdi, alb_countries)
    fdi = fdi.merge(fdi_countries, on="source_country", how="left")

    nace_group = nace[nace.level == "group"]
    nace_group["code"] = nace_group.code.astype(float)
    nace_group["code_int"] = (
        nace_group.code.astype(str).str.replace(".", "").astype(int)
    )

    fdi = fdi.merge(nace_group, on="code", how="left")[
        [
            "parent_company",
            "source_country",
            "source_city",
            "capex_world",
            "capex_europe",
            "capex_balkans",
            "projects_world",
            "projects_europe",
            "projects_balkans",
            "avg_capex",
            "avg_jobs",
            "location_id",
            "nace_id",
        ]
    ]

    fdi.to_csv(f"{PROCESSED_DATA_DIR}/fdi_markets.csv", index=False)

    # Ingest FDI over time data
    fdi_time = pd.read_csv(f"{RAW_DATA_DIR}/fDiMarkets_nace_yeargroup_march27.csv")
    fdi_time = fdi_time.merge(
        nace_group, left_on="nacecode", right_on="code", how="left"
    )[
        [
            "nace_id",
            "dest",
            "projects_03_06",
            "projects_07_10",
            "projects_11_14",
            "projects_15_18",
        ]
    ]
    fdi_time = fdi_time.rename(columns={"dest": "destination"})
    fdi_time.to_csv(f"{PROCESSED_DATA_DIR}/fdi_markets_overtime.csv", index=False)

    # Ingest Viability and Attractiveness Factors
    factors = pd.read_csv(f"{RAW_DATA_DIR}/combined_factors_april10.csv")
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
