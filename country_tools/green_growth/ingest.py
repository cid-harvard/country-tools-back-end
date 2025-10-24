import logging
import os
import pandas as pd
import sys
import numpy as np

pd.options.display.max_columns = None
pd.options.display.max_rows = None
pd.set_option("max_colwidth", 400)

logging.basicConfig(level=logging.INFO)
from green_growth.table_objects.base import Ingestion


UNIQUE_GG_4DIGIT_PRODUCTS = 195
UNIQUE_GG_CLUSTERS = 34
LAST_YEAR = 2023

INGESTION_ATTRS = {
    # "input_dir": "/n/hausmann_lab/lab/_shared_dev_data/green_growth/input/",
    # "output_dir": "/n/hausmann_lab/lab/ellie/green_growth/output/",
    "input_dir": "/home/parallels/Desktop/Parallels Shared Folders/AllFiles/Users/ELJ479/projects/green_growth/data/input/",
    "output_dir": "/home/parallels/Desktop/Parallels Shared Folders/AllFiles/Users/ELJ479/projects/green_growth/data/output/",
    "last_updated": "2025_10_14",
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

CPY_METRICS = [
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


DATA_COLUMNS = {
    "country" :
        [
            "country_id",
            "name_en",
            "name_short_en",
            "name_es",
            "name_short_es",
            "iso3_code",
            "iso2_code",
            "parent_id",
        ],
        "sc_cluster_product" : [
            "supply_chain", "product_code", "cluster_id"
        ],
        "cpysc" : [
            "year", "country_id", "product_id", "supply_chain_id", "product_ranking"
        ],
        "scatterplot" :
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
        ],
        "bar_graph_gravity" :
        [
            "year",
            "country_id",
            "product_id",
            "export_value",
            "expected_exports",
        ],
        "hexbin" : [
            "year", "country_id", "product_id", "export_rca"
        ],
        "rock_song" :
        [
            "year",
            "iso",
            "coi_green",
            "x_resid",
            "lntotnetnrexp_pc",
            "lnypc",
            "eci_all",
            "eci_green",
        ],
        "spiders" :
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
        ],
        "cluster_country_year" :[
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
            "cluster_market_share",
            "global_market_share",
        ],
        "country_rankings" :[
            "country_id",
            "year",
            "rank",
            "ranking_metric",
        ]
}

class GreenGrowthPipeline:
    def __init__(self, ingestion_attrs):
        self.ingestion_attrs = ingestion_attrs

    def run(self):
        self.GreenGrowth = Ingestion(**self.ingestion_attrs)
        self.load_data()
        self.handle_classifications()
        self.determine_green_products()
        self.prepare_supply_chain_cluster_product_member_table()
        self.prepare_country_product_year()
        self.determine_clusters()
        self.prepare_country_year()
        self.prepare_cluster_country_year()
        self.validate_data()
        self.save_data()


    def load_data(self):
        self.sc_cluster_product = self.GreenGrowth.load_parquet(
            FILE_NAME_MAP["sc_cluster_product"], self.GreenGrowth.last_updated
        )
        self.hexbin = self.GreenGrowth.load_parquet(FILE_NAME_MAP["hexbin"], self.GreenGrowth.last_updated)
        self.country = self.GreenGrowth.load_parquet("location_country", "classifications")
        self.region = self.GreenGrowth.load_parquet("location_region", "classifications")
        self.hs12_prod = self.GreenGrowth.load_parquet(
            f"product_{self.ingestion_attrs['product_classification']}",
            schema="classifications",
            filters=[("product_level", "==", self.GreenGrowth.product_level)],
        )
        # cross reference table, supply chain to cluster to 4digit product
        self.sc_cluster_product = self.GreenGrowth.load_parquet(
            FILE_NAME_MAP["sc_cluster_product"], self.GreenGrowth.last_updated
        )
        self.bar_graph_gravity = self.GreenGrowth.load_parquet(
            FILE_NAME_MAP["bar_graph_gravity"], self.GreenGrowth.last_updated
        )
        self.scatterplot = self.GreenGrowth.load_parquet(
            FILE_NAME_MAP["scatterplot"], self.GreenGrowth.last_updated
        )
        self.rock_song = self.GreenGrowth.load_parquet(
            FILE_NAME_MAP["rock_song"], self.GreenGrowth.last_updated
        )
        self.spiders = self.GreenGrowth.load_parquet(
            FILE_NAME_MAP["spiders"], self.GreenGrowth.last_updated
        )
        self.cluster_country_year = self.GreenGrowth.load_parquet(
            FILE_NAME_MAP["cluster_country_year"], self.GreenGrowth.last_updated
        )
        self.country_rankings = self.GreenGrowth.load_parquet(
            FILE_NAME_MAP["country_rankings"], self.GreenGrowth.last_updated
        )

    def handle_classifications(self):
        self.supply_chain = (
            self.hexbin["supply_chain"].drop_duplicates().reset_index(drop=True).reset_index()
        )
        self.supply_chain = self.supply_chain.rename(columns={"index": "supply_chain_id"})

        # location country classification
        self.country = self.country[(self.country.in_cp == True) & (self.country.location_level == "country")]
        self.country = self.country[DATA_COLUMNS["country"]]

        self.region = self.region.rename(columns={"id": "region_id", "regioncode": "region_code"})
        self.region = self.region.drop(columns=["abbreviation"])
        self.region = self.region[~(self.region.region_id.isna())]

    def determine_green_products(self):
        """
        Determine the green products by merging the sc_cluster_product table with the hs12_prod table.
        """
        green_prods = self.sc_cluster_product["HS2012_4dg"].unique()
        self.prod = self.hs12_prod[self.hs12_prod["code"].isin(green_prods)]

    def prepare_supply_chain_cluster_product_member_table(self):
        """
        Prepare the supply chain cluster product member table by renaming the columns and merging with the hexbin table.
        """
        self.sc_cluster_product = self.sc_cluster_product.rename(
            columns={"HS2012_4dg": "product_code", "dominant_cluster": "cluster_id"}
        )
        self.hexbin = self.hexbin.rename(columns={"HS2012": "product_code"})

        self.sc_cluster_product = self.sc_cluster_product.merge(
            self.hexbin[["product_code", "supply_chain"]],
            on="product_code",
            how="left",
        )
        self.sc_cluster_product = self.sc_cluster_product[
            DATA_COLUMNS["sc_cluster_product"]
        ]
        self.sc_cluster_product = self.sc_cluster_product.drop_duplicates()
        self.sc_cluster_product = self.sc_cluster_product.merge(
            self.supply_chain, on=["supply_chain"], how="left"
        ).merge(
            self.prod[["product_id", "code"]],
            left_on="product_code",
            right_on="code",
            how="left",
        )
        self.sc_cluster_product = self.sc_cluster_product.rename(
            columns={"id": "supply_chain_id"}
        ).drop(columns=["supply_chain", "code", "product_code"])
        self.sc_cluster_product.supply_chain_id = self.sc_cluster_product.supply_chain_id.astype(int)

    def prepare_country_product_year(self):
        """
        """
        # hexbin not supply chain specific
        self.hexbin = (
            self.hexbin.merge(
                self.country[["country_id", "name_short_en"]],
                left_on=["country_name"],
                right_on=["name_short_en"],
                how="inner",
            )
            .merge(
                self.prod[["product_id", "code"]],
                left_on="product_code",
                right_on="code",
                how="inner",
            )
            .merge(
                self.supply_chain[["supply_chain_id", "supply_chain"]],
                left_on="supply_chain",
                right_on="supply_chain",
                how="inner",
            )
        )

        self.cpysc = self.hexbin.copy()
        self.cpysc = self.cpysc.drop_duplicates(
            subset=["year", "country_id", "product_id", "supply_chain_id"]
        )
        self.cpysc = self.cpysc[
            DATA_COLUMNS["cpysc"]
        ]

        self.hexbin = self.hexbin[DATA_COLUMNS["hexbin"]]
        # hexbin = hexbin[["year", "country_id", "product_id", "normalized_export_rca"]]
        self.hexbin = self.hexbin.drop_duplicates(subset=["year", "country_id", "product_id"])
        self.hexbin = self.hexbin.rename(columns={"normalized_export_rca": "export_rca"})

        # country product year plots
        self.bar_graph_gravity = self.bar_graph_gravity.merge(
            self.country[["country_id", "iso3_code"]],
            left_on="iso3_country_id",
            right_on="iso3_code",
            how="inner",
        ).merge(
            self.prod[["product_id", "code"]], left_on="HS2012", right_on="code", how="inner"
        )
        self.bar_graph_gravity = self.bar_graph_gravity.rename(
            columns={
                "expected_exports_gravity": "expected_exports",
            }
        )
        self.bar_graph_gravity = self.bar_graph_gravity[DATA_COLUMNS["bar_graph_gravity"]]

        # scatterplot
        self.scatterplot["country_id"] = self.scatterplot["country_id"].astype(int)
        self.scatterplot["product_id"] = self.scatterplot["product_id"].astype(int)

        self.scatterplot = self.scatterplot.rename(
            columns={
                "density_std": "feasibility_std",
                "strat_balanced_portfolio": "strategy_balanced_portfolio",
                "strat_long_jump": "strategy_long_jump",
                "strat_low_hang_fruit": "strategy_low_hanging_fruit",
                "strat_frontier": "strategy_frontier",
            }
        )

        self.scatterplot = self.scatterplot.merge(
            self.country[["country_id", "iso3_code"]],
            on=["country_id", "iso3_code"],
            how="inner",
        )

        self.scatterplot = self.scatterplot[DATA_COLUMNS["scatterplot"]]
        self.scatterplot = self.scatterplot.drop_duplicates(
            subset=["year", "country_id", "product_id"]
        )

        self.cpy = self.bar_graph_gravity.merge(
            self.scatterplot,
            on=["year", "country_id", "product_id"],
            how="outer",
        ).merge(
            self.hexbin,
            on=["year", "country_id", "product_id"],
            how="outer",
        )
        # handle spider metrics
        self.spiders = self.spiders.explode("supply_chain").reset_index(drop=True)
        self.spiders["country_id"] = self.spiders["country_id"].astype(int)
        self.spiders["product_id"] = self.spiders["product_id"].astype(int)

        self.spiders = self.spiders.rename(columns={"cog": "normalized_cog", "pci": "normalized_pci"})

        self.spiders = self.spiders[DATA_COLUMNS["spiders"]]
        self.spiders = self.spiders.rename(columns={"hhi": "effective_number_of_exporters"})
        self.spiders = self.spiders.rename(
            columns={"product_mkt_share_relativepct": "product_market_share_growth"}
        )

        if not self.spiders[
            self.spiders.duplicated(subset=["year", "supply_chain", "country_id", "product_id"])
        ].empty:
            raise ValueError(
                "spiders has duplicate year, supply_chain, country_id, product_id values"
            )
        self.spiders = (
            self.spiders.merge(self.supply_chain, on=["supply_chain"], how="left")
            .rename(columns={"id": "supply_chain_id"})
            .drop(columns=["supply_chain"])
        )

        self.spiders = self.spiders.drop(columns=["supply_chain_id"])
        self.spiders = self.spiders.drop_duplicates(subset=["year", "country_id", "product_id"])
        self.cpy = self.cpy.merge(self.spiders, on=["year", "country_id", "product_id"], how="outer")

    def determine_clusters(self):
        """
        Determine the clusters by merging the cluster_country_year table with the cluster table.
        """
        self.cluster = self.cluster_country_year[["cluster_id", "cluster_name"]]
        self.cluster = self.cluster.drop_duplicates()

    def prepare_country_year(self):
        # rock song
        # to do country_id, regioncode link to country
        # QUESTION: how many countries are in rock song?
        # TODO: if rock song is at country level then make part of country table
        self.rock_song = self.rock_song.rename(columns={"analysis_year": "year"})
        self.rock_song = self.rock_song[DATA_COLUMNS["rock_song"]]
        self.rock_song = self.rock_song.merge(
            self.country[["country_id", "iso3_code"]],
            left_on=["iso"],
            right_on=["iso3_code"],
            how="right",
        )
        self.handle_policy_recommendations()
        self.rock_song = self.rock_song.drop(
            columns=["iso", "iso3_code", "eci_all", "eci_all_rank", "eci_green"]
        )

        # country rankings
        self.country_rankings = (
            self.country[["country_id", "iso3_code"]].merge(
                self.country_rankings, on="iso3_code", how="left"
            )
        )
        self.country_rankings = self.country_rankings.rename(
            columns={"country_value": "ranking_metric", "country_rank": "rank"}
        )
        self.country_rankings['rank'] = self.country_rankings.groupby(['year'])['ranking_metric'].transform('rank', ascending=False)

        self.country_rankings = self.country_rankings[DATA_COLUMNS["country_rankings"]]
        self.country_rankings = self.country_rankings.drop_duplicates(subset=["country_id", "year"])
        self.rock_song = self.rock_song.merge(self.country_rankings, on=["country_id", "year"], how="left")


    def prepare_cluster_country_year(self):
        import pdb; pdb.set_trace()
        self.cluster_country_year = self.cluster_country_year.rename(
            columns={
                "country_cluster_share": "cluster_market_share",
                "export_rca_cluster": "rca",
                "pci_std": "pci",
                "cog_std": "cog",
                "density_std": "density",
                "strat_balanced_portfolio": "strategy_balanced_portfolio",
                "strat_long_jump": "strategy_long_jump",
                "strat_low_hang_fruit": "strategy_low_hanging_fruit",
                "strat_frontier": "strategy_frontier",
                "world_cluster_share": "global_market_share"
            }
        )
        
        self.cluster_country_year = self.cluster_country_year[
            DATA_COLUMNS["cluster_country_year"]
        ]
        import pdb; pdb.set_trace()

    def validate_data(self):
        if not self.cpy[self.cpy.duplicated(subset=["year", "country_id", "product_id"])].empty:
            logging.warning("cpy has duplicates")
        missing_values = [col for col in CPY_METRICS if self.cpy[col].isna().any().any()]
        if missing_values:
            logging.warning(f"cpy has na values {missing_values}")


        # handle missing values and duplicates
        if not self.rock_song[self.rock_song.duplicated(subset=["year", "country_id"])].empty:
            raise ValueError("rock_song has duplicate iso values")
        if not self.rock_song[self.rock_song.year.isna()].empty:
            self.rock_song = self.rock_song.dropna(subset=["year"])
            # raise ValueError("rock_song has na values in year")
            logging.warning("rock_song has na values in year")
            logging.warning(self.rock_song[self.rock_song.year.isna()])
        if not self.rock_song[self.rock_song.x_resid.isna()].empty:
            logging.warning("rock_song has na values in x_resid")
            logging.warning(self.rock_song[self.rock_song.x_resid.isna()])
        if not self.rock_song[self.rock_song.coi_green.isna()].empty:
            logging.warning("rock_song has na values in coi_green")
            logging.warning(self.rock_song[self.rock_song.coi_green.isna()])

        if not self.cluster_country_year[
            self.cluster_country_year.duplicated(subset=["year", "cluster_id", "country_id"])
        ].empty:
            self.cluster_country_year = self.cluster_country_year.drop_duplicates(
                subset=["year", "cluster_id", "country_id"]
            )
            # raise ValueError("cluster_country_year has duplicate cluster and country pairs")
        if not self.cluster_country_year[
            self.cluster_country_year.pci.isna()
            | self.cluster_country_year.cog.isna()
            | self.cluster_country_year.density.isna()
            | self.cluster_country_year.rca.isna()
        ].empty:
            logging.warning(
                "cluster_country_year has na values in pci, cog, density, or rca"
            )
            logging.warning(
                self.cluster_country_year[
                    self.cluster_country_year.pci.isna()
                    | self.cluster_country_year.cog.isna()
                    | self.cluster_country_year.density.isna()
                    | self.cluster_country_year.rca.isna()
                ]
            )


        # check for inclusion at 4 digit level
        # combine assert into one?
        dataframes = [
            self.prod,
            self.cpy,
            self.hexbin,
            self.bar_graph_gravity,
            self.scatterplot,
            self.spiders,
        ]
        assert all(
            df.product_id.nunique() == UNIQUE_GG_4DIGIT_PRODUCTS for df in dataframes
        )

        # cluster
        assert self.cluster.cluster_id.nunique() == UNIQUE_GG_CLUSTERS

        # validate max year
        dataframes = [self.cpy, self.cpysc, self.cluster_country_year, self.rock_song]
        assert all(df.year.max() == LAST_YEAR for df in dataframes)


    def save_data(self):
        import pdb; pdb.set_trace()
        # save self.GreenGrowth data to output directory
        self.GreenGrowth.save_parquet(self.supply_chain, "supply_chain")
        self.GreenGrowth.save_parquet(self.country, "location_country")
        self.GreenGrowth.save_parquet(self.region, "location_region")
        self.GreenGrowth.save_parquet(self.prod, f"product_{self.GreenGrowth.product_classification}")
        self.GreenGrowth.save_parquet(self.cluster, "cluster")
        self.GreenGrowth.save_parquet(self.cluster_country_year, "cluster_country_year")
        self.GreenGrowth.save_parquet(self.sc_cluster_product, "supply_chain_cluster_product_member")
        self.GreenGrowth.save_parquet(self.cpysc, "country_product_year_supply_chain")
        self.GreenGrowth.save_parquet(self.cpy, "country_product_year")
        self.GreenGrowth.save_parquet(self.rock_song, "country_year")

    def handle_policy_recommendations(self):
        """
        # technological frontier: green growth leaders => Maintain competitive Edge => Frontier strategy
        # parsimonious industrial: well connected, low complexity => Climb the Complexity Ladder => Balanced Portfolio Strategy
        # strategic bets: emerging opportunities => Reinvent industrial base => Long Jump strategy
        # light touch: high complexity, not well connected => Harness Nearby Opportunities => Low Hanging Fruit strategy
        """
        self.rock_song["eci_all_rank"] = self.rock_song.groupby("year")["eci_all"].rank(
            ascending=False
        )
        self.rock_song["policy_recommendation"] = None
        for row in self.rock_song.itertuples():

            if row.eci_all is not None and row.eci_all_rank <= 9:
                # frontier strategy
                self.rock_song.loc[row.Index, "policy_recommendation"] = (
                    "Maintain competitive edge"
                )
                self.rock_song.loc[row.Index, "strategy"] = "Frontier"
            # Also manually assign USA to tech frontier
            elif row.country_id is not None and row.country_id == 840:
                self.rock_song.loc[row.Index, "policy_recommendation"] = (
                    "Maintain competitive edge"
                )
                self.rock_song.loc[row.Index, "strategy"] = "Frontier"
            # Otherwise bottom half is strategic bets
            elif row.coi_green <= 0.0:
                # strategic bets
                self.rock_song.loc[row.Index, "policy_recommendation"] = (
                    "Reinvent industrial base"
                )
                self.rock_song.loc[row.Index, "strategy"] = "Long jump"
            # Top half split at controlled ECI == 0.0
            elif row.x_resid >= 0.0:
                #  light touch
                self.rock_song.loc[row.Index, "policy_recommendation"] = (
                    "Harness nearby opportunities"
                )
                self.rock_song.loc[row.Index, "strategy"] = "Low hanging fruit"
            else:
                # parsimonious industrial
                self.rock_song.loc[row.Index, "policy_recommendation"] = (
                    "Climb the complexity ladder"
                )
                self.rock_song.loc[row.Index, "strategy"] = "Balanced portfolio"


if __name__ == "__main__":
    GreenGrowthPipeline = GreenGrowthPipeline(INGESTION_ATTRS)
    GreenGrowthPipeline.run()
