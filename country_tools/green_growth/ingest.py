import logging
import os
import pandas as pd
import numpy as np

pd.options.display.max_columns = None
pd.options.display.max_rows = None
pd.set_option("max_colwidth", 400)

logging.basicConfig(level=logging.INFO)
from green_growth.table_objects.base import Ingestion


UNIQUE_GG_4DIGIT_PRODUCTS = 195
LAST_YEAR = 2023

INGESTION_ATTRS = {
    # "input_dir": "/n/hausmann_lab/lab/_shared_dev_data/green_growth/input/",
    # "output_dir": "/n/hausmann_lab/lab/ellie/green_growth/output/",
    "input_dir": "/home/parallels/Desktop/Parallels Shared Folders/AllFiles/Users/ELJ479/projects/green_growth/data/input/",
    "output_dir": "/home/parallels/Desktop/Parallels Shared Folders/AllFiles/Users/ELJ479/projects/green_growth/data/output/",
    "last_updated": "2025_10_06",
    "product_classification": "hs12",
    "product_level": 4,
}

FILE_NAME_MAP = {
    "hexbin": "0_hexbin_input",
    # "supply_chain": "1_supply_chain_input",
    "bar_graph_gravity": "1_expected_actual_gravity",
    "bar_graph_rca": "2_expected_actual_rca",
    "scatterplot": "3_scatterplot_input",
    "spiders": "4_spiders",
    "sc_cluster_product": "5_product_cluster_mapping",
    "cluster_country_year": "6_cluster_country_metrics",
    "rock_song": "7_green_rock_song",
    "country_rankings": "9_country_rankings",
}

# create a dictionary of the strategy names and their descriptions
STRATEGY_DESCRIPTIONS = {
    "balanced_portfolio": "Climb the Complexity Ladder",
    "low_hanging_fruit": "Harness Nearby Opportunities",
    "frontier": "Maintain competitive Edge",
    "long_jump": "Reinvent industrial base",
}


def run(ingestion_attrs):

    GreenGrowth = Ingestion(**ingestion_attrs)

    sc_cluster_product = GreenGrowth.load_parquet(
        FILE_NAME_MAP["sc_cluster_product"], GreenGrowth.last_updated
    )
    hexbin = GreenGrowth.load_parquet(FILE_NAME_MAP["hexbin"], GreenGrowth.last_updated)

    # supply chain classification
    supply_chain = (
        hexbin["supply_chain"].drop_duplicates().reset_index(drop=True).reset_index()
    )
    supply_chain = supply_chain.rename(columns={"index": "supply_chain_id"})

    # location country classification
    country = GreenGrowth.load_parquet("location_country", "classifications")
    country = country[(country.in_cp == True) & (country.location_level == "country")]
    country = country[
        [
            "country_id",
            "name_en",
            "name_short_en",
            "name_es",
            "name_short_es",
            "iso3_code",
            "iso2_code",
            "parent_id",
        ]
    ]

    region = GreenGrowth.load_parquet("location_region", "classifications")
    region = region.rename(columns={"id": "region_id", "regioncode": "region_code"})
    region = region.drop(columns=["abbreviation"])
    # TODO which region are being dropped?
    region = region[~(region.region_id.isna())]

    # product hs12 classification
    # TODO does our product name, match gg product name

    hs12_prod = GreenGrowth.load_parquet(
        f"product_{ingestion_attrs['product_classification']}",
        schema="classifications",
        filters=[("product_level", "==", GreenGrowth.product_level)],
    )

    # cross reference table, supply chain to cluster to 4digit product
    sc_cluster_product = GreenGrowth.load_parquet(
        FILE_NAME_MAP["sc_cluster_product"], GreenGrowth.last_updated
    )

    green_prods = sc_cluster_product["HS2012_4dg"].unique()
    prod = hs12_prod[hs12_prod["code"].isin(green_prods)]

    sc_cluster_product = sc_cluster_product.rename(
        columns={"HS2012_4dg": "product_code", "dominant_cluster": "cluster_id"}
    )
    hexbin = hexbin.rename(columns={"HS2012": "product_code"})

    sc_cluster_product = sc_cluster_product.merge(
        hexbin[["product_code", "supply_chain"]],
        on="product_code",
        how="left",
    )
    sc_cluster_product = sc_cluster_product[
        ["supply_chain", "product_code", "cluster_id"]
    ]
    sc_cluster_product = sc_cluster_product.drop_duplicates()
    sc_cluster_product = sc_cluster_product.merge(
        supply_chain, on=["supply_chain"], how="left"
    ).merge(
        prod[["product_id", "code"]],
        left_on="product_code",
        right_on="code",
        how="left",
    )
    sc_cluster_product = sc_cluster_product.rename(
        columns={"id": "supply_chain_id"}
    ).drop(columns=["supply_chain", "code", "product_code"])
    sc_cluster_product.supply_chain_id = sc_cluster_product.supply_chain_id.astype(int)

    # hexbin not supply chain specific
    hexbin = (
        hexbin.merge(
            country[["country_id", "name_short_en"]],
            left_on=["country_name"],
            right_on=["name_short_en"],
            how="inner",
        )
        .merge(
            prod[["product_id", "code"]],
            left_on="product_code",
            right_on="code",
            how="inner",
        )
        .merge(
            supply_chain[["supply_chain_id", "supply_chain"]],
            left_on="supply_chain",
            right_on="supply_chain",
            how="inner",
        )
    )

    cpysc = hexbin.copy()
    cpysc = cpysc.drop_duplicates(
        subset=["year", "country_id", "product_id", "supply_chain_id"]
    )
    cpysc = cpysc[
        ["year", "country_id", "product_id", "supply_chain_id", "product_ranking"]
    ]

    hexbin = hexbin[["year", "country_id", "product_id", "export_rca"]]
    # hexbin = hexbin[["year", "country_id", "product_id", "normalized_export_rca"]]
    hexbin = hexbin.drop_duplicates(subset=["year", "country_id", "product_id"])
    hexbin = hexbin.rename(columns={"normalized_export_rca": "export_rca"})

    green_products = hexbin.product_id.unique()
    prod = prod[prod.product_id.isin(green_products)]

    # country product year plots
    bar_graph_gravity = (
        GreenGrowth.load_parquet(
            FILE_NAME_MAP["bar_graph_gravity"], GreenGrowth.last_updated
        )
        .merge(
            country[["country_id", "iso3_code"]],
            left_on="iso3_country_id",
            right_on="iso3_code",
            how="inner",
        )
        .merge(
            prod[["product_id", "code"]], left_on="HS2012", right_on="code", how="inner"
        )
    )

    bar_graph_gravity = bar_graph_gravity.rename(
        columns={
            "expected_exports_gravity": "expected_exports",
        }
    )
    bar_graph_gravity = bar_graph_gravity[
        [
            "year",
            "country_id",
            "product_id",
            "export_value",
            "expected_exports",
        ]
    ]

    # scatterplot
    scatterplot = GreenGrowth.load_parquet(
        FILE_NAME_MAP["scatterplot"], GreenGrowth.last_updated
    )

    scatterplot["country_id"] = scatterplot["country_id"].astype(int)
    scatterplot["product_id"] = scatterplot["product_id"].astype(int)

    scatterplot = scatterplot.rename(columns={"density_std": "feasibility_std"})
    scatterplot = scatterplot.rename(
        columns={
            "strat_balanced_portfolio": "strategy_balanced_portfolio",
            "strat_long_jump": "strategy_long_jump",
            "strat_low_hang_fruit": "strategy_low_hanging_fruit",
            "strat_frontier": "strategy_frontier",
        }
    )

    scatterplot = scatterplot.merge(
        country[["country_id", "iso3_code"]],
        on=["country_id", "iso3_code"],
        how="inner",
    )

    scatterplot = scatterplot[
        [
            "year",
            "country_id",
            "product_id",
            "pci_std",
            "cog_std",
            "feasibility_std",
            "strategy_balanced_portfolio",
            "strategy_long_jump",
            "strategy_low_hanging_fruit",
            "strategy_frontier",
        ]
    ]
    scatterplot = scatterplot.drop_duplicates(
        subset=["year", "country_id", "product_id"]
    )

    cpy_metrics = [
        "export_value",
        "expected_exports",
        "export_rca",
        "pci_std",
        "cog_std",
        "feasibility_std",
        "strategy_balanced_portfolio",
        "strategy_long_jump",
        "strategy_low_hanging_fruit",
        "strategy_frontier",
    ]

    cpy = bar_graph_gravity.merge(
        scatterplot,
        on=["year", "country_id", "product_id"],
        how="outer",
    ).merge(
        hexbin,
        on=["year", "country_id", "product_id"],
        how="outer",
    )

    if not cpy[cpy.duplicated(subset=["year", "country_id", "product_id"])].empty:
        logging.warning("cpy has duplicates")
    missing_values = [col for col in cpy_metrics if cpy[col].isna().any().any()]
    if missing_values:
        logging.warning(f"cpy has na values {missing_values}")

    # rock song
    # to do country_id, regioncode link to country
    # QUESTION: how many countries are in rock song?
    # TODO: if rock song is at country level then make part of country table
    rock_song = GreenGrowth.load_parquet(
        FILE_NAME_MAP["rock_song"], GreenGrowth.last_updated
    )

    rock_song = rock_song.rename(columns={"analysis_year": "year"})
    rock_song = rock_song[
        [
            "year",
            "iso",
            "coi_green",
            "x_resid",
            "lntotnetnrexp_pc",
            "lnypc",
            "eci_all",
            "eci_green",
        ]
    ]
    rock_song = rock_song.merge(
        country[["country_id", "iso3_code"]],
        left_on=["iso"],
        right_on=["iso3_code"],
        how="right",
    )  # .drop(columns=["iso", "iso3_code"])

    rock_song = handle_policy_recommendations(rock_song)

    rock_song = rock_song.drop(
        columns=["iso", "iso3_code", "eci_all", "eci_all_rank", "eci_green"]
    )

    # handle missing values and duplicates
    if not rock_song[rock_song.duplicated(subset=["year", "country_id"])].empty:
        raise ValueError("rock_song has duplicate iso values")
    if not rock_song[rock_song.year.isna()].empty:
        rock_song = rock_song.dropna(subset=["year"])
        # raise ValueError("rock_song has na values in year")
        logging.warning("rock_song has na values in year")
        logging.warning(rock_song[rock_song.year.isna()])
    if not rock_song[rock_song.x_resid.isna()].empty:
        logging.warning("rock_song has na values in x_resid")
        logging.warning(rock_song[rock_song.x_resid.isna()])
    if not rock_song[rock_song.coi_green.isna()].empty:
        logging.warning("rock_song has na values in coi_green")
        logging.warning(rock_song[rock_song.coi_green.isna()])

    # handle spider metrics
    # year, supply_chain, country, product level
    spiders = GreenGrowth.load_parquet(
        FILE_NAME_MAP["spiders"], GreenGrowth.last_updated
    )

    spiders = spiders.explode("supply_chain").reset_index(drop=True)
    spiders["country_id"] = spiders["country_id"].astype(int)
    spiders["product_id"] = spiders["product_id"].astype(int)

    spiders = spiders.rename(columns={"cog": "normalized_cog", "pci": "normalized_pci"})

    spiders = spiders[
        [
            "year",
            "supply_chain",
            "country_id",
            "product_id",
            "global_market_share",
            # "cog",
            "normalized_cog",
            "density",
            # "pci",
            "normalized_pci",
            "hhi",
            "product_market_share",
            "product_mkt_share_relativepct",
        ]
    ]

    spiders = spiders.rename(columns={"hhi": "effective_number_of_exporters"})
    spiders = spiders.rename(
        columns={"product_mkt_share_relativepct": "product_market_share_growth"}
    )

    if not spiders[
        spiders.duplicated(subset=["year", "supply_chain", "country_id", "product_id"])
    ].empty:
        raise ValueError(
            "spiders has duplicate year, supply_chain, country_id, product_id values"
        )
    spiders = (
        spiders.merge(supply_chain, on=["supply_chain"], how="left")
        .rename(columns={"id": "supply_chain_id"})
        .drop(columns=["supply_chain"])
    )

    spiders = spiders.drop(columns=["supply_chain_id"])
    spiders = spiders.drop_duplicates(subset=["year", "country_id", "product_id"])
    cpy = cpy.merge(spiders, on=["year", "country_id", "product_id"], how="outer")

    # cluster country metrics
    cluster_country_year = GreenGrowth.load_parquet(
        FILE_NAME_MAP["cluster_country_year"], GreenGrowth.last_updated
    )

    cluster = cluster_country_year[["cluster_id", "cluster_name"]]
    cluster = cluster.drop_duplicates()

    cluster_country_year = cluster_country_year.rename(
        columns={
            "export_rca_cluster": "rca",
            "pci_std": "pci",
            "cog_std": "cog",
            "density_std": "density",
            "strat_balanced_portfolio": "strategy_balanced_portfolio",
            "strat_long_jump": "strategy_long_jump",
            "strat_low_hang_fruit": "strategy_low_hanging_fruit",
            "strat_frontier": "strategy_frontier",
        }
    )
    cluster_country_year = cluster_country_year[
        [
            "year",
            "cluster_id",
            "country_id",
            "pci",
            "cog",
            "density",
            "rca",
            "export_value",
            "strategy_balanced_portfolio",
            "strategy_long_jump",
            "strategy_low_hanging_fruit",
            "strategy_frontier",
            # "global_market_share",
        ]
    ]

    if not cluster_country_year[
        cluster_country_year.duplicated(subset=["year", "cluster_id", "country_id"])
    ].empty:
        cluster_country_year = cluster_country_year.drop_duplicates(
            subset=["year", "cluster_id", "country_id"]
        )
        # raise ValueError("cluster_country_year has duplicate cluster and country pairs")
    if not cluster_country_year[
        cluster_country_year.pci.isna()
        | cluster_country_year.cog.isna()
        | cluster_country_year.density.isna()
        | cluster_country_year.rca.isna()
    ].empty:
        logging.warning(
            "cluster_country_year has na values in pci, cog, density, or rca"
        )
        logging.warning(
            cluster_country_year[
                cluster_country_year.pci.isna()
                | cluster_country_year.cog.isna()
                | cluster_country_year.density.isna()
                | cluster_country_year.rca.isna()
            ]
        )

    # country rankings
    country_rankings = GreenGrowth.load_parquet(
        FILE_NAME_MAP["country_rankings"], GreenGrowth.last_updated
    )
    country_rankings = (
        country[["country_id", "iso3_code"]].merge(
            country_rankings, on="iso3_code", how="left"
        )
        # .drop(columns=["iso3_code"])
    )
    country_rankings = country_rankings.rename(
        columns={"country_value": "ranking_metric", "country_rank": "rank"}
    )

    country_rankings = country_rankings[
        [
            "country_id",
            "year",
            "rank",
            "ranking_metric",
        ]
    ]
    country_rankings = country_rankings.drop_duplicates(subset=["country_id", "year"])
    rock_song = rock_song.merge(country_rankings, on=["country_id", "year"], how="left")

    # check for inclusion at 4 digit level
    # combine assert into one?
    dataframes = [
        prod,
        cpy,
        hexbin,
        bar_graph_gravity,
        scatterplot,
        spiders,
    ]
    assert all(
        df.product_id.nunique() == UNIQUE_GG_4DIGIT_PRODUCTS for df in dataframes
    )

    # cluster
    assert cluster.cluster_id.nunique() == 34

    # validate max year
    dataframes = [cpy, cpysc, cluster_country_year, rock_song]
    assert all(df.year.max() == LAST_YEAR for df in dataframes)

    import pdb

    pdb.set_trace()

    # save GreenGrowth data to output directory
    # classifications
    GreenGrowth.save_parquet(supply_chain, "supply_chain")
    GreenGrowth.save_parquet(country, "location_country")
    GreenGrowth.save_parquet(region, "location_region")
    GreenGrowth.save_parquet(prod, f"product_{GreenGrowth.product_classification}")
    GreenGrowth.save_parquet(cluster, "cluster")
    GreenGrowth.save_parquet(cluster_country_year, "cluster_country_year")
    GreenGrowth.save_parquet(sc_cluster_product, "supply_chain_cluster_product_member")

    # Green Growth
    GreenGrowth.save_parquet(cpysc, "country_product_year_supply_chain")
    GreenGrowth.save_parquet(cpy, "country_product_year")
    GreenGrowth.save_parquet(rock_song, "country_year")

    # save GreenGrowth data to output directory
    # classifications
    supply_chain.to_csv(
        os.path.join(GreenGrowth.output_dir, "supply_chain.csv"), index=False
    )
    country.to_csv(
        os.path.join(GreenGrowth.output_dir, "location_country.csv"), index=False
    )
    prod.to_csv(
        os.path.join(
            GreenGrowth.output_dir, f"product_{GreenGrowth.product_classification}.csv"
        ),
        index=False,
    )
    sc_cluster_product.to_csv(
        os.path.join(GreenGrowth.output_dir, "supply_chain_cluster_product_member.csv"),
        index=False,
    )
    region.to_csv(
        os.path.join(GreenGrowth.output_dir, "location_region.csv"), index=False
    )

    # Green Growth
    cpy.to_csv(
        os.path.join(GreenGrowth.output_dir, "country_product_year.csv"), index=False
    )
    cluster_country_year.to_csv(
        os.path.join(GreenGrowth.output_dir, "cluster_country_year.csv"), index=False
    )

    rock_song.to_csv(
        os.path.join(GreenGrowth.output_dir, "country_year.csv"), index=False
    )


def handle_policy_recommendations(rock_song):
    """
    # technological frontier: green growth leaders => Maintain competitive Edge => Frontier strategy
    # parsimonious industrial: well connected, low complexity => Climb the Complexity Ladder => Balanced Portfolio Strategy
    # strategic bets: emerging opportunities => Reinvent industrial base => Long Jump strategy
    # light touch: high complexity, not well connected => Harness Nearby Opportunities => Low Hanging Fruit strategy
    """
    rock_song["eci_all_rank"] = rock_song.groupby("year")["eci_all"].rank(
        ascending=False
    )
    rock_song["policy_recommendation"] = None
    for row in rock_song.itertuples():

        if row.eci_all is not None and row.eci_all_rank <= 9:
            # frontier strategy
            rock_song.loc[row.Index, "policy_recommendation"] = (
                "Maintain competitive edge"
            )
            rock_song.loc[row.Index, "strategy"] = "Frontier"
        # Also manually assign USA to tech frontier
        elif row.country_id is not None and row.country_id == 840:
            rock_song.loc[row.Index, "policy_recommendation"] = (
                "Maintain competitive edge"
            )
            rock_song.loc[row.Index, "strategy"] = "Frontier"
        # Otherwise bottom half is strategic bets
        elif row.coi_green <= 0.0:
            # strategic bets
            rock_song.loc[row.Index, "policy_recommendation"] = (
                "Reinvent industrial base"
            )
            rock_song.loc[row.Index, "strategy"] = "Long jump"
        # Top half split at controlled ECI == 0.0
        elif row.x_resid >= 0.0:
            #  light touch
            rock_song.loc[row.Index, "policy_recommendation"] = (
                "Harness nearby opportunities"
            )
            rock_song.loc[row.Index, "strategy"] = "Low hanging fruit"
        else:
            # parsimonious industrial
            rock_song.loc[row.Index, "policy_recommendation"] = (
                "Climb the complexity ladder"
            )
            rock_song.loc[row.Index, "strategy"] = "Balanced portfolio"
    return rock_song


if __name__ == "__main__":
    run(INGESTION_ATTRS)
