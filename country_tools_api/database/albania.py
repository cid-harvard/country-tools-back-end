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
from sqlalchemy.orm import relationship


class NACEIndustry(Base):

    __tablename__ = "nace_industry"

    nace_id = Column(String, primary_key=True)
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
    __table_args__ = (PrimaryKeyConstraint("nace_id", "destination"), {})

    nace_id = Column(Integer)
    destination = Column(
        Enum(*["Balkans", "Rest of Europe", "Rest of World"], name="destination")
    )
    projects_03_06 = Column(Integer)
    projects_07_10 = Column(Integer)
    projects_11_14 = Column(Integer)
    projects_15_18 = Column(Integer)


class Factors(Base):

    __tablename__ = "factors"

    nace_id = Column(Integer, primary_key=True)
    rca = Column(Enum(*[">= 1", "< 1"], name="rca"))
    v_rca = Column(Integer)
    v_dist = Column(Integer)
    v_fdipeers = Column(Integer)
    v_contracts = Column(Integer)
    v_elect = Column(Integer)
    avg_viability = Column(Float)
    a_youth = Column(Integer)
    a_wage = Column(Integer)
    a_fdiworld = Column(Integer)
    a_export = Column(Integer)
    avg_attractiveness = Column(Float)
    v_text = Column(String)
    a_text = Column(String)
    rca_text1 = Column(String)
    rca_text2 = Column(String)


class Script(Base):

    __tablename__ = "script"
    __table_args__ = (PrimaryKeyConstraint("section", "subsection"), {})

    section = Column(String)
    subsection = Column(String)
    text = Column(String)
