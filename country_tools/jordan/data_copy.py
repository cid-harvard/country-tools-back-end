import pandas as pd
from sqlalchemy import MetaData, event
from sqlalchemy.schema import CreateSchema
from pandas_to_postgres import DataFrameCopy
from country_tools.country_tools_api.database.base import engine, Base
from country_tools.country_tools_api.database.jordan import (
    JordanNationality,
    JordanControl,
    JordanText,
    JordanOccupation,
    JordanSchooling,
    JordanWageHistogram,
    JordanMapLocation,
    JordanGlobalTopFDI,
    JordanRegionTopFDI,
    JordanFactors,
    JordanIndustry,
)


JOR_SCHEMA = "jordan"
JOR_PROCESSED_DATA_DIR = "./jordan/processed_data"
JOR_TABLES = [
    "control",
    "factors",
    "global_top_fdi",
    "industry",
    "map_location",
    "nationality",
    "occupation",
    "over_time",
    "region_top_fdi",
    "schooling",
    "text",
    "wage_histogram",
]


if __name__ == "__main__":
    engine.execute(f"CREATE SCHEMA IF NOT EXISTS {JOR_SCHEMA};")
    Base.metadata.create_all()

    with engine.connect() as c:
        meta = MetaData(bind=c, reflect=True, schema=JOR_SCHEMA)

        for table in JOR_TABLES:
            DataFrameCopy(
                pd.read_csv(f"{JOR_PROCESSED_DATA_DIR}/{table}.csv"),
                conn=c,
                table_obj=meta.tables[f"{JOR_SCHEMA}.{table}"],
            ).copy()
