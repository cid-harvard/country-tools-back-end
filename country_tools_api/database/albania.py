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


class NACEIndustry(Base):

    __tablename__ = "nace_industry"

    nace_id = Column(Integer, primary_key=True)
    level = Column(Enum(*["section", "division", "group"], name="industry_level"))
    code = Column(String)
    name = Column(String)
    parent_id = Column(Integer)


class Country(Base):

    __tablename__ = "country"

    location_id = Column(Integer, primary_key=True)
    code = Column(String)
    level = Column(Enum(*["region", "country"], name="location_level"))
    name_en = Column(String)
    name_short_en = Column(String)
    iso2 = Column(String)
    parent_id = Column(Integer)
    name = Column(String)
    is_trusted = Column(Boolean(create_constraint=False), nullable=True)
    in_rankings = Column(Boolean(create_constraint=False), nullable=True)
    reported_serv = Column(Boolean(create_constraint=False), nullable=True)
    reported_serv_recent = Column(Boolean(create_constraint=False), nullable=True)
    former_country = Column(Boolean(create_constraint=False), nullable=True)


class FDIMarkets(Base):

    __tablename__ = "fdi_markets"
    __table_args__ = (
        PrimaryKeyConstraint(
            "nace_id", "parent_company", "source_city", "source_country"
        ),
        {},
    )

    nace_id = Column(Integer)
    location_id = Column(Integer)
    parent_company = Column(String)
    source_country = Column(String)
    source_city = Column(String)
    capex_world = Column(Float)
    capex_europe = Column(Float)
    capex_balkans = Column(Float)
    projects_world = Column(Integer)
    projects_europe = Column(Integer)
    projects_balkans = Column(Integer)


class FDIMarketsOvertime(Base):

    __tablename__ = "fdi_markets_overtime"

    nace_id = Column(Integer, primary_key=True)
    destination = Column(
        Enum(*["balkans", "rest_europe", "rest_world"], name="destination")
    )
    projects_03_06 = Column(Integer)
    projects_07_10 = Column(Integer)
    projects_11_14 = Column(Integer)
    projects_15_18 = Column(Integer)


class Viability(Base):

    __tablename__ = "viability"

    nace_id = Column(Integer, primary_key=True)
    score_rca = Column(Integer)
    score_dist = Column(Integer)
    score_fdipeers = Column(Integer)
    score_contracts = Column(Integer)


# class Attractiveness(Base):

#     __tablename__ = "attractiveness"
