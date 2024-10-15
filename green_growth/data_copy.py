import pandas as pd
import os
from sqlalchemy import MetaData, event
from sqlalchemy.schema import CreateSchema
from pandas_to_postgres import DataFrameCopy
from country_tools_api.database.base import engine, Base
from country_tools_api.database.green_growth import (
    GGCountryProductYear,
    GGSupplyChainProductMember,
    GGSupplyChain,
    GGLocationCountry,
    GGProduct,
)
from green_growth.ingest import INGESTION_ATTRS


OUTPUT_DIR = os.path.join(INGESTION_ATTRS['output_dir'], INGESTION_ATTRS['last_updated'])
DATA_MODELS = ["country_product_year", "supply_chain_product_member","supply_chain","location_country","product"]
SCHEMA = "green_growth"
    
    
def copy():
    """
    """
    engine.execute(f"CREATE SCHEMA IF NOT EXISTS green_growth;")
    Base.metadata.create_all()


    with engine.connect() as c:
        meta = MetaData(bind=c, reflect=True, schema=SCHEMA)

    print("****************************************")
    print(f"Data Directory: {OUTPUT_DIR}")
    print(f"Database Connection: {engine}")
    print("****************************************")
        

    for table in DATA_MODELS:
        DataFrameCopy(
            pd.read_parquet(os.path.join(OUTPUT_DIR, f"{table}.parquet")),
            conn=c,
            table_obj=meta.tables[f"{SCHEMA}.{table}"],
        ).copy()


if __name__ == "__main__":
    copy()
    
