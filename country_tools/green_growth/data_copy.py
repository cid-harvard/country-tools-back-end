# poetry remove graphene-sqlalchemy
# poetry add sqlalchemy@2
# to get back to running api
# poetry add sqlalchemy@1.4
# poetry add graphene-sqlalchemy

import pandas as pd
import argparse
import os
from sqlalchemy import MetaData, event, text, INTEGER, exc
from sqlalchemy.schema import CreateSchema
from pandas_to_postgres import DataFrameCopy, ParquetCopy, cast_pandas

from country_tools.country_tools_api.database.base import engine, Base

from country_tools.country_tools_api.database.greenplexity import (
    GPCountryProductYear,
    GPSupplyChain,
    GPLocationCountry,
    GPLocationRegion,
    GPProduct,
    GPSupplyChainClusterProductMember,
    GPClusterCountryYear,
    GPCountryYear,
    GPCluster,
    GPCountryProductYearSupplyChain,
)
from country_tools.green_growth.ingest import INGESTION_ATTRS


OUTPUT_DIR = os.path.join(
    INGESTION_ATTRS["output_dir"], INGESTION_ATTRS["last_updated"]
)
DATA_MODELS = [
    "country_product_year",
    "country_year",
    "country_product_year_supply_chain",
    "supply_chain_cluster_product_member",
    "supply_chain",
    "location_country",
    "location_region",
    "product_hs12",
    "cluster_country_year",
    "cluster",
]
SCHEMA = "greenplexity"

parser = argparse.ArgumentParser()
parser.add_argument("--tables", nargs="+", default=DATA_MODELS)
args = parser.parse_args()


def copy():
    """ """
    print("****************************************")
    print(f"Data Directory: {OUTPUT_DIR}")
    print(f"Database Connection: {engine}")
    print("****************************************")

    import pdb
    pdb.set_trace()

    with engine.connect() as conn:
        conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA};"))
        conn.commit()

    # Base.metadata.clear()
    Base.metadata.create_all(bind=engine)

    with engine.connect() as conn:
        meta = MetaData()
        meta.reflect(bind=conn, schema=SCHEMA)

        for table in args.tables:
            ParquetCopy(
                os.path.join(OUTPUT_DIR, f"{table}.parquet"),
                conn=conn,
                table_obj=meta.tables[f"{SCHEMA}.{table}"],
            ).copy()


if __name__ == "__main__":
    copy()
