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

    DataFrameCopy(
        pd.read_csv("./albania/processed_data/fdi_markets_overtime.csv"),
        conn=c,
        table_obj=meta.tables["fdi_markets_overtime"],
    ).copy()

    DataFrameCopy(
        pd.read_csv("./albania/processed_data/factors.csv"),
        conn=c,
        table_obj=meta.tables["factors"],
    ).copy()

    DataFrameCopy(
        pd.read_csv("./albania/processed_data/albania_script.csv"),
        conn=c,
        table_obj=meta.tables["script"],
    ).copy()
