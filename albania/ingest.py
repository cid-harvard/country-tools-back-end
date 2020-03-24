import pandas as pd
from linnaeus import classification

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
    nace = classification.load("industry/NACE/Albania/out/nace_industries.csv")
    alb_countries = classification.load(
        "location/International/Atlas/out/locations_international_atlas.csv"
    ).table

    alb_countries = pd.concat([alb_countries, ADDITIONAL_COUNTRIES])

    fdi = pd.read_csv("./raw_data/FDI_Markets_for_filters.csv")
    fdi.columns = [
        "subsector",
        "parent_company",
        "source_country",
        "source_city",
        "capex_world",
        "capex_europe",
        "capex_balkans",
        "projects_world",
        "projects_europe",
        "projects_balkans",
    ]

    fdi_countries = fdi_countries_to_loc_class(fdi, alb_countries)

    fdi = fdi.merge(fdi_countries, on="source_country", how="left")
