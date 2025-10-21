import pandas as pd
from sqlalchemy import MetaData, event
from sqlalchemy.schema import CreateSchema
from pandas_to_postgres import DataFrameCopy
from country_tools.country_tools_api.database.base import engine, Base
from country_tools.country_tools_api.database.namibia import (
    NamibiaHSClassification,
    NamibiaNAICSClassification,
)


NAM_SCHEMA = "namibia"
NAM_PROCESSED_DATA_DIR = "./namibia/processed_data"
NAM_TABLES = [
    "hs_classification",
    "hs_factors",
    "hs_occupation",
    "hs_proximity",
    "hs_relative_demand",
    "naics_classification",
    "naics_factors",
    "naics_occupation",
    "naics_proximity",
    "naics_relative_demand",
    "threshold",
]


if __name__ == "__main__":
    engine.execute(f"CREATE SCHEMA IF NOT EXISTS {NAM_SCHEMA};")
    Base.metadata.create_all()

    with engine.connect() as c:
        meta = MetaData(bind=c, reflect=True, schema=NAM_SCHEMA)

        for table in NAM_TABLES:
            DataFrameCopy(
                pd.read_csv(f"{NAM_PROCESSED_DATA_DIR}/{table}.csv"),
                conn=c,
                table_obj=meta.tables[f"{NAM_SCHEMA}.{table}"],
            ).copy()
