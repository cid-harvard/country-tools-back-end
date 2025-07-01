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

# from sqlalchemy.orm import relation, relationship, foreign


class GGSupplyChainClusterProductMember(Base):
    __tablename__ = "supply_chain_cluster_product_member"
    __table_args__ = (
        PrimaryKeyConstraint("supply_chain_id", "cluster_id", "product_id"),
        {"schema": "greenplexity"},
    )
    supply_chain_id = Column(
        Integer, primary_key=True
    )  # , ForeignKey('SupplyChain.supply_chain_id'))
    product_id = Column(
        Integer, primary_key=True
    )  # , ForeignKey('Product.product_id'))
    cluster_id = Column(Integer, primary_key=True)


class GGCountryProductYear(Base):
    __tablename__ = "country_product_year"
    __table_args__ = (
        PrimaryKeyConstraint("country_id", "product_id", "year"),
        {"schema": "greenplexity"},
    )
    year = Column(Integer, primary_key=True)
    country_id = Column(Integer, primary_key=True)
    product_id = Column(Integer, primary_key=True)
    export_rca = Column(Float)
    export_value = Column(Float)
    expected_exports = Column(Float)
    feasibility_std = Column(Float)
    pci_std = Column(Float)
    cog_std = Column(Float)
    balanced_portfolio = Column(Float)
    global_market_share = Column(Float)
    normalized_cog = Column(Float)
    density = Column(Float)
    normalized_pci = Column(Float)
    product_market_share = Column(Float)
    effective_number_of_exporters = Column(Float)
    product_market_share_growth = Column(Float)


class GGCountryProductYearSupplyChain(Base):
    __tablename__ = "country_product_year_supply_chain"
    __table_args__ = (
        PrimaryKeyConstraint("country_id", "product_id", "year", "supply_chain_id"),
        {"schema": "greenplexity"},
    )
    year = Column(Integer, primary_key=True)
    country_id = Column(Integer, primary_key=True)
    product_id = Column(Integer, primary_key=True)
    supply_chain_id = Column(Integer, primary_key=True)
    product_ranking = Column(Integer)


class GGCountryYear(Base):
    __tablename__ = "country_year"
    __table_args__ = (
        PrimaryKeyConstraint("country_id", "year"),
        {"schema": "greenplexity"},
    )
    country_id = Column(Integer, primary_key=True)
    year = Column(Integer, primary_key=True)
    coi_green = Column(Float)
    lntotnetnrexp_pc = Column(Float)
    lnypc = Column(Float)
    x_resid = Column(Float)


class GGClusterCountryYear(Base):
    __tablename__ = "cluster_country_year"
    __table_args__ = (
        PrimaryKeyConstraint("cluster_id", "country_id", "year"),
        {"schema": "greenplexity"},
    )
    cluster_id = Column(Integer, primary_key=True)
    country_id = Column(Integer, primary_key=True)
    year = Column(Integer, primary_key=True)
    pci = Column(Float)
    cog = Column(Float)
    density = Column(Float)
    rca = Column(Float)
    export_value = Column(Float)
    global_market_share = Column(Float)


class GGSupplyChain(Base):
    __tablename__ = "supply_chain"
    __table_args__ = ({"schema": "greenplexity"},)
    supply_chain_id = Column(Integer, primary_key=True)
    supply_chain = Column(String)


class GGCluster(Base):
    __tablename__ = "cluster"
    __table_args__ = ({"schema": "greenplexity"},)
    cluster_id = Column(Integer, primary_key=True)
    cluster_name = Column(String)
    member_cluster = relationship(
        "GGSupplyChainClusterProductMember",
        primaryjoin=(
            cluster_id == foreign(GGSupplyChainClusterProductMember.cluster_id)
        ),
    )


class GGLocationRegion(Base):
    __tablename__ = "location_region"
    __table_args__ = ({"schema": "greenplexity"},)
    region_id = Column(Integer, primary_key=True)
    name = Column(String)
    region_code = Column(String)
    country_id = Column(Integer)


class GGLocationCountry(Base):
    __tablename__ = "location_country"
    __table_args__ = ({"schema": "greenplexity"},)

    country_id = Column(Integer, primary_key=True)
    # location_level = Column(String(50))
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
    rankings_override = Column(Boolean)
    cp_override = Column(Boolean)
    incomelevel_enum = Column(Text)
    country_project = Column(Boolean)
    parent_id = Column(Integer)
    country = relationship(
        "GGCountryProductYear",
        primaryjoin=(country_id == foreign(GGCountryProductYear.country_id)),
    )


class GGProduct(Base):
    __tablename__ = "product_hs12"
    __table_args__ = ({"schema": "greenplexity"},)

    product_id = Column(Integer, primary_key=True)
    code = Column(String(6))
    name_en = Column(String)
    name_short_en = Column(String)
    product_level = Column(Integer)
    parent_id = Column(Integer)
    product_id_hierarchy = Column(String)
    top_parent_id = Column(Integer)
    show_feasibility = Column(Boolean)
