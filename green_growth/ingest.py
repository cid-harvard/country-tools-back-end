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
        "last_updated": "2025_04_30",
        "product_classification": "hs12",
        "product_level": 4,   
    }


def run(ingestion_attrs):
    
    GreenGrowth = Ingestion(**ingestion_attrs)
    
    # green_prods_hs92 = GreenGrowth.load_parquet("0_green_prods_92", GreenGrowth.last_updated)
    sc_cluster_product = GreenGrowth.load_parquet("5_product_cluster_mapping", GreenGrowth.last_updated)
    hexbin = GreenGrowth.load_parquet("1_hexbin_input", GreenGrowth.last_updated)
    

    # supply chain classification
    supply_chain = sc_cluster_product['supply_chain'].drop_duplicates().reset_index(drop=True).reset_index()
    supply_chain = supply_chain.rename(columns={"index": "id"})    
    
    # location country classification
    country = GreenGrowth.load_parquet("location_country", "classifications")
    country = country[(country.in_cp==True) & (country.location_level=="country")]
    country = country[['country_id', 'name_en', 'name_short_en', 'name_es', 
                       'name_short_es', 'iso3_code', 'iso2_code', 'parent_id']]

    region = GreenGrowth.load_parquet("location_region", "classifications")
    
    # product hs12 classification
    # TODO does our product name, match gg product name
    prod = GreenGrowth.load_parquet(f"product_{ingestion_attrs['product_classification']}", 
                                    schema="classifications",
                                    filters=[('product_level', "==", GreenGrowth.product_level)]
                                   )
    # cluster classification
    cluster = GreenGrowth.load_parquet("manufacturing_cluster", schema = "classifications")
    cluster = cluster.rename(columns={"dominant_cluster": "cluster_id"})

    # cross reference table, supply chain to cluster to 4digit product
    sc_cluster_product = GreenGrowth.load_parquet("5_product_cluster_mapping", GreenGrowth.last_updated)
    sc_cluster_product = sc_cluster_product.drop_duplicates(subset=['product_id','dominant_cluster'])
    sc_cluster_product = sc_cluster_product[['supply_chain', 'product_id', 'dominant_cluster']]
    sc_cluster_product = sc_cluster_product.merge(supply_chain, on=["supply_chain"], how="left")
    sc_cluster_product = sc_cluster_product.rename(columns={"id":"supply_chain_id","dominant_cluster": "cluster_id"})
    sc_cluster_product.supply_chain_id = sc_cluster_product.supply_chain_id.astype(int)

    # scp = hexbin[['supply_chain','HS2012']].groupby(["supply_chain", "HS2012"]).agg("first").reset_index()
    # scp = scp.merge(supply_chain, on=["supply_chain"], how="left")
    # scp = scp.merge(prod[['product_id', 'code']], left_on="HS2012", right_on="code", how="left")
    # scp = scp.rename(columns={"id":"supply_chain_id"}).drop(columns=["supply_chain", "code", "HS2012"])    

    
    # hexbin not supply chain specific
    hexbin = hexbin.merge(country[['country_id', 'name_short_en']], left_on=['country_name'], right_on=['name_short_en'], how="inner").merge(prod[['product_id', 'code']], left_on="HS2012", right_on="code", how="inner")
    hexbin = hexbin[["year", "country_id", "product_id", "normalized_export_rca", "product_ranking"]]    
    
    green_products = hexbin.product_id.unique()
    prod = prod[prod.product_id.isin(green_products)]
        
    # country product year plots
    bar_graph = GreenGrowth.load_parquet("2_expected_actual", GreenGrowth.last_updated).merge(country[['country_id', 'iso3_code']], on=['iso3_code'], how="inner").merge(prod[['product_id', 'code']], left_on="HS2012", right_on="code", how="inner")
    bar_graph = bar_graph[["year", "country_id", "product_id", "export_value", "expected_exports"]]
    bar_graph = bar_graph.drop_duplicates(subset=['year', 'country_id', 'product_id'])
    
    # scatterplot
    scatterplot = GreenGrowth.load_parquet("3_scatterplot_input", GreenGrowth.last_updated).merge(country[['country_id', 'iso3_code']], on=['iso3_code'], how="inner").merge(prod[['product_id', 'code']], left_on="HS2012", right_on="code", how="inner").merge(supply_chain, on=["supply_chain"], how="left").rename(columns={"id":"supply_chain_id"})
    scatterplot = scatterplot[["year", "country_id", "product_id", "export_rca", "pci_std", "cog_std", "feasibility_std", "balanced_portfolio"]]
    scatterplot = scatterplot.drop_duplicates(subset=['year', 'country_id', 'product_id'])

    cpy_metrics = ["export_value", "expected_exports", "export_rca", "pci_std", "cog_std", "feasibility_std", "balanced_portfolio", "normalized_export_rca", "product_ranking"]
    cpy = bar_graph.merge(scatterplot, on=["year","country_id", "product_id"], how="outer").merge(hexbin[["year", "country_id", "product_id", "normalized_export_rca", "product_ranking"]], on=["year", "country_id", "product_id"], how="outer")
    if not cpy[cpy.duplicated(subset=['year', 'country_id', 'product_id'])].empty:
        logging.warning("cpy has duplicates")
    missing_values = [col for col in cpy_metrics if cpy[col].isna().any()]
    if missing_values:
        logging.warning(f"cpy has na values {missing_values}")
        
    # rock song
    # to do country_id, regioncode link to country
    # QUESTION: how many countries are in rock song?
    # TODO: if rock song is at country level then make part of country table
    rock_song = GreenGrowth.load_parquet("6_green_rock_song", GreenGrowth.last_updated)
    rock_song = rock_song[["iso","coi_green", "x_resid"]]
    rock_song = rock_song.merge(country[['country_id', 'iso3_code']], left_on=['iso'], right_on=['iso3_code'], how="outer").drop(columns=["iso", "iso3_code"])
    # handle missing values and duplicates
    if not rock_song[rock_song.duplicated(subset='country_id')].empty:
        raise ValueError("rock_song has duplicate iso values")
    if not rock_song[rock_song.x_resid.isna()].empty:
        logging.warning("rock_song has na values in x_resid")
        logging.warning(rock_song[rock_song.x_resid.isna()])
    if not rock_song[rock_song.coi_green.isna()].empty:
        logging.warning("rock_song has na values in coi_green")
        logging.warning(rock_song[rock_song.coi_green.isna()])



    # handle spider metrics
    #year, supply_chain, country, product level 
    spiders = GreenGrowth.load_parquet("4_spiders", GreenGrowth.last_updated)
    spiders = spiders.drop_duplicates()
    spiders = spiders.merge(country[['country_id', 'name_short_en']], left_on=['country_name'], right_on=['name_short_en'], how="inner").merge(prod[['product_id', 'code']], left_on="HS2012", right_on="code", how="inner")
    
    spiders = spiders[["year", "supply_chain", "country_id", "product_id", "global_market_share", "normalized_cog",
                     "density", "normalized_pci", "effective_number_of_exporters", "product_market_share_growth"]]
    if not spiders[spiders.duplicated(subset=["year", "supply_chain", "country_id", "product_id"])].empty:
        raise ValueError("spiders has duplicate year, supply_chain, country_id, product_id values")
    spiders = spiders.merge(supply_chain, on=["supply_chain"], how="left").rename(columns={"id":"supply_chain_id"}).drop(columns=["supply_chain"])


    cpy = cpy.merge(spiders, on=["year", "country_id", "product_id"], how="outer")  


    # cluster country metrics
    cluster_country = GreenGrowth.load_parquet("7_cluster_country_metrics", GreenGrowth.last_updated)
    cluster_country = cluster_country.rename(columns={"dominant_cluster": "cluster_id"})
    cluster_country = cluster_country[["cluster_id", "country_id", "pci", "cog", "density", "rca"]]
    
    if not cluster_country[cluster_country.duplicated(subset=['cluster_id', 'country_id'])].empty:
        raise ValueError("cluster_country has duplicate cluster and country pairs")
    if not cluster_country[cluster_country.pci.isna() | cluster_country.cog.isna() | cluster_country.density.isna() | cluster_country.rca.isna()].empty:
        logging.warning("cluster_country has na values in pci, cog, density, or rca")
        logging.warning(cluster_country[cluster_country.pci.isna() | cluster_country.cog.isna() | cluster_country.density.isna() | cluster_country.rca.isna()])

    # check for inclusion
    assert prod.product_id.nunique() == 210
    assert cpy.product_id.nunique() == 210
    assert hexbin.product_id.nunique() == 210
    assert bar_graph.product_id.nunique() == 210
    assert scatterplot.product_id.nunique() == 210
    assert spiders.product_id.nunique() == 210
    

    # save GreenGrowth data to output directory
    # classifications
    GreenGrowth.save_parquet(supply_chain, "supply_chain")
    GreenGrowth.save_parquet(country, "location_country")
    GreenGrowth.save_parquet(prod, f"product_{GreenGrowth.product_classification}")
    GreenGrowth.save_parquet(sc_cluster_product, "supply_chain_cluster_product_member")
    GreenGrowth.save_parquet(cluster, "cluster")
    
    # Green Growth 
    # GreenGrowth.save_parquet(cpy_sc, "country_product_year_supply_chain", "green_growth")
    GreenGrowth.save_parquet(cpy, "country_product_year")
    
    
    # save GreenGrowth data to output directory
    # classifications
    supply_chain.to_csv(os.path.join(GreenGrowth.output_dir, "supply_chain.csv"), index=False)
    country.to_csv(os.path.join(GreenGrowth.output_dir, "location_country.csv"), index=False)
    prod.to_csv(os.path.join(GreenGrowth.output_dir, f"product_{GreenGrowth.product_classification}.csv"), index=False)
    sc_cluster_product.to_csv(os.path.join(GreenGrowth.output_dir, "supply_chain_cluster_product_member.csv"), index=False)
    region.to_csv(os.path.join(GreenGrowth.output_dir, "location_region.csv"), index=False)

    # Green Growth 
    cpy.to_csv(os.path.join(GreenGrowth.output_dir, "country_product_year.csv"), index=False)
    cluster_country.to_csv(os.path.join(GreenGrowth.output_dir, "cluster_country.csv"), index=False)
    rock_song.to_csv(os.path.join(GreenGrowth.output_dir, "country.csv"), index=False)
    import pdb; pdb.set_trace()

if __name__ == "__main__":
    run(INGESTION_ATTRS)
