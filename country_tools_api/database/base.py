from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
import os

# Create database engine
db_user = "postgres"
db_pass = ""
db_host = "country-tools-staging.cppjqzftxysd.us-east-1.rds.amazonaws.com"
db_name = "country_tools"
db_uri = f"postgresql://{db_user}:{db_pass}@{db_host}/{db_name}"
engine = create_engine(db_uri, convert_unicode=True)

# Declarative base model to create database tables and classes
Base = declarative_base()
Base.metadata.bind = engine  # Bind engine to metadata of the base class

# Create database session object
db_session = scoped_session(sessionmaker(bind=engine, expire_on_commit=False))
Base.query = db_session.query_property()  # Used by graphql to execute queries
