import pandas as pd
import os
from sqlalchemy import MetaData, event, text, INTEGER, exc
from sqlalchemy.schema import CreateSchema
from pandas_to_postgres import DataFrameCopy, ParquetCopy, cast_pandas

from country_tools.country_tools_api.database.base import engine, Base

from country_tools.country_tools_api.database.green_growth import (
    GGCountryProductYear,
    GGSupplyChainProductMember,
    GGSupplyChain,
    GGLocationCountry,
    GGProduct,
)
from green_growth.ingest import INGESTION_ATTRS


OUTPUT_DIR = os.path.join(
    INGESTION_ATTRS["output_dir"], INGESTION_ATTRS["last_updated"]
)
DATA_MODELS = [
    "country_product_year",
    "country_product_year_supply_chain",
    "supply_chain_product_member",
    "supply_chain",
    "location_country",
    "product",
]
SCHEMA = "green_growth"


def copy():
    """ """
    print("****************************************")
    print(f"Data Directory: {OUTPUT_DIR}")
    print(f"Database Connection: {engine}")
    print("****************************************")

    with engine.connect() as conn:
        conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA};"))
        conn.commit()

    Base.metadata.create_all(bind=engine)

    with engine.connect() as conn:
        meta = MetaData()
        meta.reflect(bind=conn, schema=SCHEMA)

        for table in DATA_MODELS:

            ParquetCopy(
                os.path.join(OUTPUT_DIR, f"{table}.parquet"),
                conn=conn,
                table_obj=meta.tables[f"{SCHEMA}.{table}"],
            ).copy()


if __name__ == "__main__":
    copy()
