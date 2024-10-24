import sys
import pandas as pd
from sqlalchemy import MetaData, event
from sqlalchemy.schema import CreateSchema
from pandas_to_postgres import DataFrameCopy
from country_tools.country_tools_api.database.base import engine, Base
from country_tools.country_tools_api.database.albania import (
    AlbaniaNACEIndustry,
    AlbaniaCountry,
    AlbaniaFDIMarkets,
    AlbaniaFDIMarketsOvertime,
    AlbaniaFactors,
    AlbaniaScript,
)

ALB_SCHEMA = "albania"
ALB_PROCESSED_DATA_DIR = "./albania/processed_data"
ALB_TABLES = [
    "country",
    "nace_industry",
    "fdi_markets",
    "fdi_markets_overtime",
    "factors",
    "script",
    "industry_now_location",
    "industry_now_schooling",
    "industry_now_occupation",
    "industry_now_wage",
    "industry_now_nearest_industry",
]


if __name__ == "__main__":
    table_args = sys.argv[1:]
    if table_args != []:
        tables = table_args
    else:
        tables = ALB_TABLES

    engine.execute(f"CREATE SCHEMA IF NOT EXISTS {ALB_SCHEMA};")
    Base.metadata.create_all()

    with engine.connect() as c:
        meta = MetaData(bind=c, reflect=True, schema=ALB_SCHEMA)

        for table in tables:
            DataFrameCopy(
                pd.read_csv(f"{ALB_PROCESSED_DATA_DIR}/{table}.csv"),
                conn=c,
                table_obj=meta.tables[f"{ALB_SCHEMA}.{table}"],
            ).copy()
