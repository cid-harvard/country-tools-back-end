from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
import os

# Create database engine
db_user = os.environ.get("COUNTRY_TOOLS_DB_USER")
db_pass = os.environ.get("COUNTRY_TOOLS_DB_PASS")
db_host = os.environ.get("COUNTRY_TOOLS_DB_HOST")
db_name = os.environ.get("COUNTRY_TOOLS_DB_NAME")
db_uri = f"postgresql://{db_user}:{db_pass}@{db_host}/{db_name}"
engine = create_engine(db_uri, convert_unicode=True)

# Declarative base model to create database tables and classes
Base = declarative_base()
Base.metadata.bind = engine  # Bind engine to metadata of the base class

# Create database session object
db_session = scoped_session(sessionmaker(bind=engine, expire_on_commit=False))
Base.query = db_session.query_property()  # Used by graphql to execute queries