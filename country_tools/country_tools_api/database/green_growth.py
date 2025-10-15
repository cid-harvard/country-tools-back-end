from .base import Base
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Text,
    Boolean,
    Enum,
    Float,
    PrimaryKeyConstraint,
    ForeignKeyConstraint,
)
from sqlalchemy.orm import relationship, foreign


class GGSupplyChain(Base):
    __tablename__ = "supply_chain"
    __table_args__ = {"schema": "green_growth"}
    supply_chain_id = Column(Integer, primary_key=True)
    supply_chain = Column(String, primary_key=True)


class GGProduct(Base):
    __tablename__ = "product"
    __table_args__ = {"schema": "green_growth"}
    product_id = Column(Integer, primary_key=True)
    code = Column(String(6))
    name_en = Column(String)
    name_short_en = Column(String)
    product_level = Column(Integer)
    parent_id = Column(Integer)
    product_id_hierarchy = Column(String)
    top_parent_id = Column(Integer)
    show_feasibility = Column(Boolean)


class GGLocationCountry(Base):
    __tablename__ = "location_country"
    __table_args__ = {"schema": "green_growth"}
    country_id = Column(Integer, primary_key=True)
    name_en = Column(String(100))
    name_short_en = Column(String(50))
    name_es = Column(String(100))
    name_short_es = Column(String(50))
    iso3_code = Column(String(3))
    iso2_code = Column(String(2))
    legacy_location_id = Column(Integer)
    parent_id = Column(Integer)
    name_abbr_en = Column(String(50))
    the_prefix = Column(Boolean)
    former_country = Column(Boolean)
    rankings_override = Column(Boolean)
    cp_override = Column(Boolean)
    incomelevel_enum = Column(Text)
    country_project = Column(Boolean)


class GGSupplyChainProductMember(Base):
    __tablename__ = "supply_chain_product_member"
    __table_args__ = {"schema": "green_growth"}
    supply_chain_id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey(GGProduct.product_id), primary_key=True)
    supply_chain = relationship(
        "GGSupplyChain",
        primaryjoin=(supply_chain_id == foreign(GGSupplyChain.supply_chain_id)),
    )
    product = relationship(
        "GGProduct",
        primaryjoin=(product_id == foreign(GGProduct.product_id)),
    )


class GGCountryProductYear(Base):
    __tablename__ = "country_product_year"
    __table_args__ = {"schema": "green_growth"}
    year = Column(Integer, primary_key=True)
    country_id = Column(Integer, primary_key=True)
    product_id = Column(Integer, primary_key=True)
    export_rca = Column(Float)
    normalized_export_rca = Column(Float)
    export_value = Column(Float)
    expected_exports = Column(Float)
    normalized_pci = Column(Float)  # spider metrics (5)
    normalized_cog = Column(Float)
    feasibility = Column(Float)
    effective_number_of_exporters = Column(Float)
    market_growth = Column(Float)
    pci_std = Column(Float)  # standardized values are for the scatterplot visualization
    cog_std = Column(Float)
    feasibility_std = Column(Float)
    pci_cog_feasibility_composite = Column(Float)
    location = relationship(
        "GGLocationCountry",
        primaryjoin=(country_id == foreign(GGLocationCountry.country_id)),
    )
    product = relationship(
        "GGProduct",
        primaryjoin=(product_id == foreign(GGProduct.product_id)),
    )


class GGCountryProductYearSupplyChain(Base):
    __tablename__ = "country_product_year_supply_chain"
    __table_args__ = {"schema": "green_growth"}
    year = Column(Integer, primary_key=True)
    country_id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey(GGProduct.product_id), primary_key=True)
    supply_chain_id = Column(Integer, primary_key=True)
    product_ranking = Column(Integer)
    location = relationship(
        "GGLocationCountry",
        primaryjoin=(country_id == foreign(GGLocationCountry.country_id)),
    )