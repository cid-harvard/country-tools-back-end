import logging
import os
import pandas as pd

pd.options.display.max_columns = None
pd.options.display.max_rows = None
pd.set_option("max_colwidth", 400)

logging.basicConfig(level=logging.INFO)
# from green_growth.table_objects.base import Ingestion
from green_growth.table_objects.base import Ingestion



INGESTION_ATTRS = {
        "input_dir": "/n/hausmann_lab/lab/_shared_dev_data/green_growth/input/",
        "output_dir": "/n/hausmann_lab/lab/_shared_dev_data/green_growth/output/",
        "last_updated": "2024_10_14",
        "product_classification": "hs12",
        "product_level": 4,
        
    }


def run(ingestion_attrs):
    
    GreenGrowth = Ingestion(**ingestion_attrs)
    
    hexbin = GreenGrowth.load_parquet("1_hexbin_input", GreenGrowth.last_updated)
    
    # supply chain classification
    supply_chain = hexbin['supply_chain'].drop_duplicates().reset_index(drop=True).reset_index()
    supply_chain = supply_chain.rename(columns={"index": "id"})    
    
    # location country classification
    country = GreenGrowth.load_parquet("location_country", "classifications")
    
    # product hs12 classification
    # TODO does our product name, match gg product name
    prod = GreenGrowth.load_parquet(f"product_{ingestion_attrs['product_classification']}", 
                                    schema="classifications",
                                    filters=[('product_level', "==", GreenGrowth.product_level)]
                                   )
    
    # cross reference table
    supply_chain_product_member = hexbin[['supply_chain','HS2012']].groupby(["supply_chain", "HS2012"]).agg("first").reset_index()
    supply_chain_product_member = supply_chain_product_member.merge(supply_chain, on=["supply_chain"], how="left")
    supply_chain_product_member = supply_chain_product_member.merge(prod[['product_id', 'code']], left_on="HS2012", right_on="code", how="left")
    supply_chain_product_member = supply_chain_product_member.rename(columns={"id":"supply_chain_id"}).drop(columns=["supply_chain", "code", "HS2012"])    

    
    # hexbin not supply chain specific
    hexbin = hexbin.merge(country[['country_id', 'name_short_en']], left_on=['country_name'], right_on=['name_short_en'], how="left").merge(prod[['product_id', 'code']], left_on="HS2012", right_on="code", how="left")
        
    hexbin = hexbin[["year", "country_id", "product_id", "export_rca", "normalized_export_rca", "product_ranking"]]    
    hexbin = hexbin.drop_duplicates(subset=['year', 'country_id', 'product_id'])
    
    # country product year
    # year | country_id | product_id | export_value | expected_exports | export_rca | feasibility | attractiveness
    # normalized_export_rca | product_ranking
        
    bar_graph = GreenGrowth.load_parquet("2_expected_actual", GreenGrowth.last_updated).merge(country[['country_id', 'iso3_code']], on=['iso3_code'], how="left").merge(prod[['product_id', 'code']], left_on="HS2012", right_on="code", how="left")
    bar_graph = bar_graph[["year", "country_id", "product_id", "export_value", "expected_exports"]]
    bar_graph = bar_graph.drop_duplicates(subset=['year', 'country_id', 'product_id'])
    
    # scatterplot
    scatterplot = GreenGrowth.load_parquet("3_scatterplot_input", GreenGrowth.last_updated).merge(country[['country_id', 'iso3_code']], on=['iso3_code'], how="left").merge(prod[['product_id', 'code']], left_on="HS2012", right_on="code", how="left").merge(supply_chain, on=["supply_chain"], how="left").rename(columns={"id":"supply_chain_id"})
    
    scatterplot = scatterplot[["year", "country_id", "product_id", "supply_chain_id", "feasibility", "attractiveness"]]
    scatterplot = scatterplot.drop_duplicates(subset=['year', 'country_id', 'product_id'])
    
    cpy = hexbin.merge(bar_graph, on=["year", "country_id", "product_id"], how="left").merge(scatterplot, on=["year", "country_id", "product_id"], how="left")
        
    # save GreenGrowth data to output directory
    # classifications
    GreenGrowth.save_parquet(supply_chain, "supply_chain")
    GreenGrowth.save_parquet(country, "location_country")
    GreenGrowth.save_parquet(prod, f"product_{GreenGrowth.product_classification}")
    GreenGrowth.save_parquet(supply_chain_product_member, "supply_chain_product_member")
    
    # Green Growth 
    # GreenGrowth.save_parquet(cpy_sc, "country_product_year_supply_chain", "green_growth")
    GreenGrowth.save_parquet(cpy, "country_product_year")
    
    
    # save GreenGrowth data to output directory
    # classifications
    supply_chain.to_csv(os.path.join(GreenGrowth.output_dir, "supply_chain.csv"), index=False)
    country.to_csv(os.path.join(GreenGrowth.output_dir, "location_country.csv"), index=False)
    prod.to_csv(os.path.join(GreenGrowth.output_dir, f"product_{GreenGrowth.product_classification}.csv"), index=False)
    supply_chain_product_member.to_csv(os.path.join(GreenGrowth.output_dir, "supply_chain_product_member.csv"), index=False)
    
    # Green Growth 
    cpy.to_csv(os.path.join(GreenGrowth.output_dir, "country_product_year.csv"), index=False)
    
    
if __name__ == "__main__":
    run(INGESTION_ATTRS)
