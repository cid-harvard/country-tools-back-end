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


class SupplyChainProductMember(Base):
    __tablename__ = 'supply_chain_product_member'
    __table_args__ = (
        PrimaryKeyConstraint("supply_chain_id", "product_id"),
        {"schema": "green_growth"},
    )
    supply_chain_id = Column(Integer, primary_key=True)#, ForeignKey('SupplyChain.supply_chain_id'))
    product_id = Column(Integer, primary_key=True)#, ForeignKey('Product.product_id'))

    
class CountryProductYear(Base):
    __tablename__ = 'country_product_year'
    __table_args__ = (
        PrimaryKeyConstraint("country_id", "product_id", "year"),
        {"schema": "green_growth"},
    )
    year = Column(Integer, primary_key=True)
    country_id = Column(Integer, primary_key=True)#, ForeignKey('location_country.country_id'))
    product_id = Column(Integer, primary_key=True)#, ForeignKey('product.product_id'))
    export_rca = Column(Float)
    normalized_export_rca = Column(Float)
    product_ranking = Column(Integer)
    export_value = Column(Float)
    expected_exports = Column(Float)
    # feasibility = Column(Float)
    # attractiveness = Column(Float)



class SupplyChain(Base):
    __tablename__ = 'supply_chain'
    __table_args__ = ({"schema": "green_growth"},)
    supply_chain_id = Column(Integer, primary_key=True)
    supply_chain = Column(String, primary_key=True)
    member_supply_chain = relationship(
        "SupplyChainProductMember", primaryjoin=(supply_chain_id == foreign(SupplyChainProductMember.supply_chain_id))
    )

class LocationCountry(Base):
    __tablename__ = 'location_country'
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
        "CountryProductYear", primaryjoin=(country_id == foreign(CountryProductYear.country_id))
    )



class Product(Base):
    __tablename__ = 'product'
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
        "CountryProductYear", primaryjoin=(product_id == foreign(CountryProductYear.product_id))
    )
    member_product = relationship(
        "SupplyChainProductMember", primaryjoin=(product_id == foreign(SupplyChainProductMember.product_id))
    )

# class CountryProductYearSupplyChain(Base):
#     __tablename__ = 'country_product_year_supply_chain'
#     __table_args__ = (
#         PrimaryKeyConstraint("country_id", "product_id", "supply_chain_id", "year"),
#         {"schema": "green_growth"},
#     )

#     year = Column(Integer)
#     country_id = Column(Integer, ForeignKey('location_country.country_id'))
#     product_id = Column(Integer, ForeignKey('product.product_id'))
#     supply_chain_id = Column(Integer, ForeignKey('supply_chain.supply_chain_id'))
#     export_rca = Column(Float)
#     feasibility = Column(Float)
#     attractiveness = Column(Float)




