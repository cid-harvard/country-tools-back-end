import pandas as pd
import os
from sqlalchemy import MetaData, event
from sqlalchemy.schema import CreateSchema
from pandas_to_postgres import DataFrameCopy
from country_tools_api.database.base import engine, Base
from country_tools_api.database.green_growth import (
    # CountryProductYearSupplyChain,
    CountryProductYear,
    SupplyChainProductMember,
    SupplyChain,
    LocationCountry,
    Product,
)
from green_growth.ingest import INGESTION_ATTRS


OUTPUT_DIR = os.path.join(INGESTION_ATTRS['output_dir'], INGESTION_ATTRS['last_updated'])
DATA_MODELS = {
    "green_growth" : ["country_product_year"], #"country_product_year_supply_chain",
    "classification": ["supply_chain_product_member","supply_chain","location_country","product"],
}
    
    
def copy():
    """
    """
    for schema, tables in DATA_MODELS.items():
        engine.execute(f"CREATE SCHEMA IF NOT EXISTS green_growth;")
        Base.metadata.create_all()
        

        with engine.connect() as c:
            meta = MetaData(bind=c, reflect=True, schema=schema)
            
        print("****************************************")
        print(f"Data Directory: {OUTPUT_DIR}")
        print(f"Database Connection: {engine}")
        print("****************************************")
        
        for table in tables:
            DataFrameCopy(
                pd.read_parquet(os.path.join(OUTPUT_DIR, schema, f"{table}.parquet")),
                conn=c,
                table_obj=meta.tables[f"green_growth.{table}"],
            ).copy()


if __name__ == "__main__":
    copy()
    
