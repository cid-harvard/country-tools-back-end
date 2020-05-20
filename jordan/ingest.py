import pandas as pd
from itertools import product

RAW_DATA_DIR = "./raw_data"
PROCESSED_DATA_DIR = "./processed_data"

# "jordanmap.json"


if __name__ == "__main__":
    ### INDUSTRY -----------------------------------------------------------------------
    industry = pd.read_csv(f"{RAW_DATA_DIR}/industry.csv")
    industry.columns = (
        "industry_code",
        "title",
        "theme",
        "subtheme",
        "description",
        "keywords",
    )
    industry.to_csv(f"{PROCESSED_DATA_DIR}/industry.csv", index=False)

    ### NATIONALITY --------------------------------------------------------------------
    nationality = pd.DataFrame(
        product(
            list(industry.industry_code),
            ["Jordanian", "Egyptian", "Syrian", "Other Arab", "Non Arab"],
        ),
        columns=("industry_code", "nationality"),
    )
    nationality_sheets = ["demographics", "wage"]

    for sheet in nationality_sheets:
        df = pd.read_csv(f"{RAW_DATA_DIR}/{sheet}.csv")
        df.columns = [x.lower() for x in df.columns]
        nationality = nationality.merge(
            df,
            how="left",
            left_on=["industry_code", "nationality"],
            right_on=["industry", "nationality"],
        )
        nationality = nationality.drop(columns=["industry"])
    nationality.to_csv(f"{PROCESSED_DATA_DIR}/nationality.csv", index=False)

    ### CONTROL ------------------------------------------------------------------------
    control_sheets = ["laborControl", "womenControl", "fdiControl"]
    control = industry[["industry_code"]]

    for sheet in control_sheets:
        df = pd.read_csv(f"{RAW_DATA_DIR}/{sheet}.csv", index_col="industry")[
            ["control"]
        ]
        df.columns = (sheet.split("Control")[0],)
        control = control.merge(
            df, how="left", left_on="industry_code", right_index=True
        )
    control.to_csv(f"{PROCESSED_DATA_DIR}/control.csv", index=False)

    ### TEXT ---------------------------------------------------------------------------
    text = industry[["industry_code"]]
    text_sheets = {
        "occupationText": ("occupation",),
        "otherText": ("demographic", "location", "avg_wage"),
        "wagehistogramText": ("wage_hist",),
        "scatterText": ("scatter",),
        "schoolingText": ("schooling",),
        # womentext combines female participation and high-skill jobs
        "womentext": ("percent_female", "percent_high_skill", "female", "high_skill"),
    }

    for sheet, cols in text_sheets.items():
        df = pd.read_csv(f"{RAW_DATA_DIR}/{sheet}.csv", index_col="industry").drop(
            columns=["sic4_description", "text1"], errors="ignore"
        )
        df.columns = cols
        text = text.merge(df, how="left", left_on="industry_code", right_index=True)
    text.to_csv(f"{PROCESSED_DATA_DIR}/text.csv", index=False)

    ### TOP FDI ------------------------------------------------------------------------
    top_fdi_sheets = {
        "FDItop10global": "global_top_fdi",
        "FDItop10region": "region_top_fdi",
    }
    for sheet, new_sheet in top_fdi_sheets.items():
        df = pd.read_csv(f"{RAW_DATA_DIR}/{sheet}.csv").drop(
            columns=["sic4_description", "total_company_capinv", "industries119"],
            errors="ignore",
        )
        df.columns = (
            "industry_code",
            "company",
            "source_country",
            "capital_investment",
            "rank",
        )
        df.to_csv(f"{PROCESSED_DATA_DIR}/{new_sheet}.csv", index=False)

    ### FACTORS ------------------------------------------------------------------------
    factors = industry[["industry_code"]]
    factor_sheets = {
        "spider": {
            "cols": (
                "industry_code",
                "rca_jordan",
                "rca_peers",
                "water_intensity",
                "electricity_intensity",
                "availability_inputs",
                "female_employment",
                "high_skill_employment",
                "fdi_world",
                "fdi_region",
                "export_propensity",
            )
        },
        "scatter": {
            "drop": ["Theme", "Subtheme", "Description"],
            "cols": (
                "industry_code",
                "viability",
                "attractiveness",
                "viability_median",
                "attractiveness_median",
                "category",
                "rca",
            ),
        },
    }
    for sheet, config in factor_sheets.items():
        df = pd.read_csv(f"{RAW_DATA_DIR}/{sheet}.csv").drop(
            columns=config.get("drop", []), errors="ignore"
        )
        df.columns = config["cols"]
        factors = factors.merge(df, how="left", on="industry_code")
    factors.to_csv(f"{PROCESSED_DATA_DIR}/factors.csv", index=False)

    ### OVER TIME ----------------------------------------------------------------------

    over_time = pd.DataFrame(
        columns=[
            "industry_code",
            "visualization",
            "variable",
            "years_2004_2006",
            "years_2007_2009",
            "years_2010_2012",
            "years_2013_2015",
            "years_2016_2018",
        ]
    )

    over_time_sheets = {"fdiBarChart": "fdi_bar_chart", "histogram": "histogram"}

    for sheet, viz_title in over_time_sheets.items():
        df = (
            pd.read_csv(f"{RAW_DATA_DIR}/{sheet}.csv")
            .drop(
                columns=[
                    "sic4_description",
                    "IndustrySector",
                    "SubSector",
                    "industrysector",
                    "subsector",
                ],
                errors="ignore",
            )
            .rename(
                columns={
                    "industry": "industry_code",
                    "Variable": "variable",
                    "2004-2006": "years_2004_2006",
                    "2007-2009": "years_2007_2009",
                    "2010-2012": "years_2010_2012",
                    "2013-2015": "years_2013_2015",
                    "2016-2018": "years_2016_2018",
                }
            )
        )
        df["visualization"] = viz_title
        over_time = over_time.append(df)

    over_time.to_csv(f"{PROCESSED_DATA_DIR}/over_time.csv", index=False)

    ### COPY OTHER SHEETS --------------------------------------------------------------
    copy_sheets = {
        "mapLocation": {
            "columns": (
                "industry_code",
                "gov_code",
                "governorate",
                "share_state",
                "share_country",
            ),
            "filename": "map_location",
        },
        "occupation": {"columns": ("industry_code", "occupation", "men", "women")},
        "schooling": {"columns": ("industry_code", "schooling", "men", "women")},
        "wagehistogram": {
            ## TODO: Duped Country row for every industry
            "columns": (
                "industry_code",
                "facet",
                "range_0_100",
                "range_100_200",
                "range_200_300",
                "range_300_400",
                "range_400_500",
                "range_500_600",
                "range_600_plus",
            ),
            "filename": "wage_histogram",
        },
    }

    for in_file, config in copy_sheets.items():
        df = pd.read_csv(f"{RAW_DATA_DIR}/{in_file}.csv")
        df.columns = config["columns"]
        out_file = config.get("filename", in_file)
        df.to_csv(f"{PROCESSED_DATA_DIR}/{out_file}.csv", index=False)
