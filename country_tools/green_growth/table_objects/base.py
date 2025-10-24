import os
import typing
import pandas as pd
import numpy as np


class Ingestion(object):
    def __init__(
        self,
        input_dir: str,
        output_dir: str,
        last_updated: str,
        product_classification="hs12",
        product_level=4,
    ):

        self.input_dir = input_dir
        self.product_classification = product_classification
        self.product_level = product_level
        self.output_dir = os.path.join(output_dir, last_updated)
        self.last_updated = last_updated

        os.makedirs(self.output_dir, exist_ok=True)

    def load_parquet(
        self,
        table_name: str,
        schema: typing.Optional[str] = None,
        filters: typing.Optional[object] = None,
        dask_df: bool = False,
        df_type: typing.Optional[str] = None,
    ):
        if schema is not None:
            read_dir = os.path.join(self.input_dir, schema)
        else:
            read_dir = os.path.join(self.input_dir)

        if dask_df:
            return dd.read_parquet(
                os.path.join(read_dir, f"{table_name}.parquet"), filters=filters
            )
        else:
            return pd.read_parquet(
                os.path.join(read_dir, f"{table_name}.parquet"), filters=filters
            )

    def load_csv(
        self,
        table_name: str,
        schema: typing.Optional[str] = None,
        filters: typing.Optional[object] = None,
        dask_df: bool = False,
    ):
        if schema is not None:
            read_dir = os.path.join(self.input_dir, schema)
        else:
            read_dir = os.path.join(self.input_dir)

        return pd.read_csv(os.path.join(read_dir, f"{table_name}.csv"))

    def save_parquet(
        self,
        df: pd.DataFrame,
        table_name: str,
        schema: typing.Optional[str] = None,
    ):
        if schema is not None:
            save_dir = os.path.join(self.output_dir, schema)
        else:
            save_dir = os.path.join(self.output_dir)

        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, f"{table_name}.parquet")
        df.to_parquet(save_path, index=False)
