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
from sqlalchemy.orm import relation, relationship, foreign


class GGSupplyChainProductMember(Base):
    __tablename__ = "supply_chain_product_member"
    __table_args__ = (
        PrimaryKeyConstraint("supply_chain_id", "product_id"),
        {"schema": "green_growth"},
    )
    supply_chain_id = Column(
        Integer, primary_key=True
    )  # , ForeignKey('SupplyChain.supply_chain_id'))
    product_id = Column(
        Integer, primary_key=True
    )  # , ForeignKey('Product.product_id'))


class GGCountryProductYear(Base):
    __tablename__ = "country_product_year"
    __table_args__ = (
        PrimaryKeyConstraint("country_id", "product_id", "year"),
        {"schema": "green_growth"},
    )
    year = Column(Integer, primary_key=True)
    country_id = Column(
        Integer, primary_key=True
    )  # , ForeignKey('location_country.country_id'))
    product_id = Column(
        Integer, primary_key=True
    )  # , ForeignKey('product.product_id'))
    export_rca = Column(Float)
    normalized_export_rca = Column(Float)
    product_ranking = Column(Integer)
    export_value = Column(Float)
    expected_exports = Column(Float)
    feasibility = Column(Float)
    attractiveness = Column(Float)


class GGSupplyChain(Base):
    __tablename__ = "supply_chain"
    __table_args__ = ({"schema": "green_growth"},)
    supply_chain_id = Column(Integer, primary_key=True)
    supply_chain = Column(String, primary_key=True)
    member_supply_chain = relationship(
        "GGSupplyChainProductMember",
        primaryjoin=(
            supply_chain_id == foreign(GGSupplyChainProductMember.supply_chain_id)
        ),
    )


class GGLocationCountry(Base):
    __tablename__ = "location_country"
    __table_args__ = ({"schema": "green_growth"},)

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
    country = relationship(
        "GGCountryProductYear",
        primaryjoin=(country_id == foreign(GGCountryProductYear.country_id)),
    )


class GGProduct(Base):
    __tablename__ = "product"
    __table_args__ = ({"schema": "green_growth"},)

    product_id = Column(Integer, primary_key=True)
    code = Column(String(6))
    name_en = Column(String)
    name_short_en = Column(String)
    product_level = Column(Integer)
    parent_id = Column(Integer)
    product_id_hierarchy = Column(String)
    top_parent_id = Column(Integer)
    show_feasibility = Column(Boolean)
    product = relationship(
        "GGCountryProductYear",
        primaryjoin=(product_id == foreign(GGCountryProductYear.product_id)),
    )
    member_product = relationship(
        "GGSupplyChainProductMember",
        primaryjoin=(product_id == foreign(GGSupplyChainProductMember.product_id)),
    )