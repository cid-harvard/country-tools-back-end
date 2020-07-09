import pandas as pd
from sqlalchemy import MetaData, event
from sqlalchemy.schema import CreateSchema
from pandas_to_postgres import DataFrameCopy
from country_tools_api.database.base import engine, Base
from country_tools_api.database.hub import HubProjects


HUB_SCHEMA = "hub"
HUB_PROCESSED_DATA_DIR = "./hub/processed_data"
HUB_TABLES = ["projects"]


if __name__ == "__main__":
    engine.execute(f"CREATE SCHEMA IF NOT EXISTS {HUB_SCHEMA};")
    Base.metadata.create_all()

    with engine.connect() as c:
        meta = MetaData(bind=c, reflect=True, schema=HUB_SCHEMA)

        for table in HUB_TABLES:
            DataFrameCopy(
                pd.read_csv(f"{HUB_PROCESSED_DATA_DIR}/{table}.csv"),
                conn=c,
                table_obj=meta.tables[f"{HUB_SCHEMA}.{table}"],
            ).copy()
