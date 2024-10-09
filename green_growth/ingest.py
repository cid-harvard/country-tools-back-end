import logging
import os
import pandas as pd

logging.basicConfig(level=logging.INFO)

def run(ingestion_attrs):
    
    df = pd.read_parquet(os.path.join(ingestion_attrs['data_dir'], "1_hexbin_input.parquet"))
    
    # supply chain classification
    supply_chain = df['supply_chain'].drop_duplicates().reset_index(drop=True).reset_index()
    supply_chain = supply_chain.rename(columns={"index": "id"})    
    
    # product hs12 classification
    prod = pd.read_parquet(os.path.join(ingestion_attrs['data_dir'], f"product_{ingestion_attrs['product_classification']}.parquet"))
    prod = prod[prod.product_level==ingestion_attrs['product_level']]
    
    # cross reference table
    supply_chain_product_member = df[['supply_chain','HS2012']].groupby(["supply_chain", "HS2012"]).agg("first").reset_index()
    supply_chain_product_member = supply_chain_product_member.merge(supply_chain, on=["supply_chain"], how="outer")
    supply_chain_product_member = supply_chain_product_member.merge(prod[['product_id', 'code']], left_on="HS2012", right_on="code", how="outer")
    supply_chain_product_member = supply_chain_product_member.rename(columns={"id":"supply_chain_id"}).drop(columns=["supply_chain", "code", "HS2012"])    
    
    
    # country product year

    
    
    
    
    
if __name__ == "__main__":
    ingestion_attrs = {
        "earliest_year": 2012,
        "latest_year": 2022,
        "product_classification": "hs12",
        "product_level": 4,
        "schema": "green_green",
        "data_dir": "/n/hausmann_lab/lab/_shared_dev_data/green_growth/input/2024_10_08/",
        "output_dir": "/n/hausmann_lab/lab/_shared_dev_data/green_growth/output/",
    }
    run(ingestion_attrs)
