import pandas as pd
import os
from sqlalchemy import MetaData, event, text
from sqlalchemy.schema import CreateSchema
from pandas_to_postgres import DataFrameCopy, ParquetCopy, cast_pandas
from country_tools_api.database.base import engine, Base
from country_tools_api.database.green_growth import (
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
    "supply_chain_product_member",
    "supply_chain",
    "location_country",
    "product",
    "country_product_year_supply_chain",
]
SCHEMA = "green_growth"


def copy():
    """ """
    print("****************************************")
    print(f"Data Directory: {OUTPUT_DIR}")
    print(f"Database Connection: {engine}")
    print("****************************************")

    engine.execute(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA};")
    Base.metadata.create_all()

    with engine.connect() as c:
        meta = MetaData(bind=c, reflect=True, schema=SCHEMA)

        for table in DATA_MODELS:
            DataFrameCopy(
                pd.read_csv(os.path.join(f"{OUTPUT_DIR}", f"{table}.csv")),
                conn=c,
                table_obj=meta.tables[f"{SCHEMA}.{table}"],
            ).copy()

    # with engine.connect() as conn:
    #     conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA};"))
    #     # conn.commit()

    # Base.metadata.create_all(conn)

    # # engine.execute(text(f"CREATE SCHEMA IF NOT EXISTS green_growth;"))
    # # Base.metadata.create_all()
    # with engine.connect() as c:
    #     meta = MetaData()
    #     meta.reflect(bind=c, schema=SCHEMA)

    #     # meta = MetaData(bind=c, reflect=True, schema=SCHEMA)

    #     for table in DATA_MODELS:
    #         print(f"{SCHEMA}/{table}.parquet")

    #         table_obj = meta.tables[f"{SCHEMA}.{table}"]
    #         file_path = os.path.join(OUTPUT_DIR, f"{table}.parquet")

    #         ParquetCopy(file_path, conn=conn, table_obj=table_obj).copy()


if __name__ == "__main__":
    copy()
