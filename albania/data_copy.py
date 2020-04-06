import pandas as pd
from pandas_to_postgres import DataFrameCopy
from country_tools_api.database.base import engine
from sqlalchemy import MetaData


with engine.connect() as c:
    meta = MetaData(bind=c, reflect=True)

    DataFrameCopy(
        pd.read_csv("./albania/processed_data/country.csv"),
        conn=c,
        table_obj=meta.tables["country"],
    ).copy()

    DataFrameCopy(
        pd.read_csv("./albania/processed_data/nace_industry.csv"),
        conn=c,
        table_obj=meta.tables["nace_industry"],
    ).copy()

    DataFrameCopy(
        pd.read_csv("./albania/processed_data/fdi_markets.csv"),
        conn=c,
        table_obj=meta.tables["fdi_markets"],
    ).copy()
