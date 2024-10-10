from .base import Base
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Boolean,
    Enum,
    Float,
    PrimaryKeyConstraint,
    ForeignKeyConstraint,
)
from sqlalchemy.orm import relation, relationship, foreign


class CountryProductYearSupplyChain(Base):
    __tablename__ = 'country_product_year_supply_chain'
    __table_args__ = (
        PrimaryKeyConstraint("country_id", "product_id", "supply_chain_id", "year"),
        {"schema": "green_growth"},
    )

    year = Column(Integer)
    country_id = Column(Integer, ForeignKey('countries.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    supply_chain_id = Column(Integer, ForeignKey('supply_chains.id'))
    export_rca = Column(Float)
    feasibility = Column(Float)
    attractiveness = Column(Float)


class CountryProductYear(Base):
    __tablename__ = 'country_product_year'
    __table_args__ = (
        PrimaryKeyConstraint("country_id", "product_id", "year"),
        {"schema": "green_growth"},
    )

    year = Column(Integer)
    country_id = Column(Integer, ForeignKey('countries.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    export_rca = Column(Float)
    normalized_export_rca = Column(Float)
    product_ranking = Column(Integer)
    export_value = Column(Float)
    expected_exports = Column(Float)

class SupplyChainProductMember(Base):
    __tablename__ = 'supply_chain_product_member'
    __table_args__ = (
        PrimaryKeyConstraint("supply_chain_id", "product_id"),
        {"schema": "green_growth"},
    )

    supply_chain_id = Column(Integer, ForeignKey('supply_chains.id'))
    product_id = Column(Integer, ForeignKey('products.id'))


class SupplyChain(Base):
    __tablename__ = 'supply_chains'
    __table_args__ = ({"schema": "green_growth"},)

    id = Column(Integer, primary_key=True)
    supply_chain = Column(String(100))


class Country(Base):
    __tablename__ = 'countries'
     __table_args__ = ({"schema": "green_growth"},)

    country_id = Column(Integer, primary_key=True)
    location_level = Column(String(50))
    name_en = Column(String(100))
    name_short_en = Column(String(50))
    name_es = Column(String(100))
    name_short_es = Column(String(50))
    iso3_code = Column(String(3))
    iso2_code = Column(String(2))
    legacy_location_id = Column(Integer)
    name_abbr_en = Column(String(50))
    the_prefix = Column(Boolean)
    former_country = Column(Boolean)
    rankings_override = Column(String(100))
    cp_override = Column(String(100))
    incomelevel_enum = Column(String(50))
    country_project = Column(Boolean)

class Product(Base):
    __tablename__ = 'products'
     __table_args__ = ({"schema": "green_growth"},)

    product_id = Column(Integer, primary_key=True)
    code = Column(String(10))
    name_en = Column(String(200))
    name_short_en = Column(String(100))
    product_level = Column(Integer)
    parent_id = Column(Integer, ForeignKey('products.product_id'))
    product_id_hierarchy = Column(String(100))
    top_parent_id = Column(Integer)
    show_feasibility = Column(Boolean)
