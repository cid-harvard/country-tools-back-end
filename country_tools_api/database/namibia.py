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


class NamibiaHSFactors(Base):
    __tablename__ = "hs_factors"
    __table_args__ = {"schema": "namibia"}

    hs_id = Column(Integer, primary_key=True)
    a_relative_demand = Column(Float)
    a_resiliency = Column(Float)
    a_employment_groups_interest = Column(Float)
    a_fdi = Column(Float)
    a_export_propensity = Column(Float)
    f_port_propensity = Column(Float)
    f_existing_presence = Column(Float)
    f_remoteness = Column(Float)
    f_scarce_factors = Column(Float)
    f_input_availability = Column(Float)
    attractiveness = Column(Float)
    feasibility = Column(Float)
    rca = Column(Float)
    share_female = Column(Float)
    share_youth = Column(Float)
    share_lskill = Column(Float)
    pct_occupations_present = Column(Float)


class NamibiaNAICSFactors(Base):
    __tablename__ = "naics_factors"
    __table_args__ = {"schema": "namibia"}

    naics_id = Column(Integer, primary_key=True)
    a_relative_demand = Column(Float)
    a_resiliency = Column(Float)
    a_employment_groups_interest = Column(Float)
    a_fdi = Column(Float)
    a_export_propensity = Column(Float)
    f_port_propensity = Column(Float)
    f_existing_presence = Column(Float)
    f_remoteness = Column(Float)
    f_scarce_factors = Column(Float)
    f_input_availability = Column(Float)
    attractiveness = Column(Float)
    feasibility = Column(Float)
    rca = Column(Float)
    share_female = Column(Float)
    share_youth = Column(Float)
    share_lskill = Column(Float)
    pct_occupations_present = Column(Float)


class NamibiaHSRelativeDemand(Base):
    __tablename__ = "hs_relative_demand"
    __table_args__ = (
        PrimaryKeyConstraint("hs_id", "location_code"),
        {"schema": "namibia"},
    )

    hs_id = Column(Integer)
    location_code = Column(String)
    country_demand_avg = Column(Float)
    country_demand_pc_avg = Column(Float)


class NamibiaNAICSRelativeDemand(Base):
    __tablename__ = "naics_relative_demand"
    __table_args__ = (
        PrimaryKeyConstraint("naics_id", "location_code"),
        {"schema": "namibia"},
    )

    naics_id = Column(Integer)
    location_code = Column(String)
    country_demand_avg = Column(Float)
    country_demand_pc_avg = Column(Float)


class NamibiaHSOccupation(Base):
    __tablename__ = "hs_occupation"
    __table_args__ = (
        PrimaryKeyConstraint("hs_id", "occupation"),
        {"schema": "namibia"},
    )

    hs_id = Column(Integer)
    occupation = Column(String)
    is_available = Column(Boolean)
    rank = Column(Integer)


class NamibiaNAICSOccupation(Base):
    __tablename__ = "naics_occupation"
    __table_args__ = (
        PrimaryKeyConstraint("naics_id", "occupation"),
        {"schema": "namibia"},
    )

    naics_id = Column(Integer)
    occupation = Column(String)
    is_available = Column(Boolean)
    rank = Column(Integer)


class NamibiaHSProximity(Base):
    __tablename__ = "hs_proximity"
    __table_args__ = (
        PrimaryKeyConstraint("hs_id", "partner_id"),
        {"schema": "namibia"},
    )

    hs_id = Column(Integer)
    partner_id = Column(Integer)
    proximity = Column(Float)
    rank = Column(Integer)
    factors = relationship(
        "NamibiaHSFactors", primaryjoin=(partner_id == foreign(NamibiaHSFactors.hs_id))
    )


class NamibiaNAICSProximity(Base):
    __tablename__ = "naics_proximity"
    __table_args__ = (
        PrimaryKeyConstraint("naics_id", "partner_id"),
        {"schema": "namibia"},
    )

    naics_id = Column(Integer)
    partner_id = Column(Integer)
    proximity = Column(Float)
    rank = Column(Integer)
    factors = relationship(
        "NamibiaNAICSFactors",
        primaryjoin=(partner_id == foreign(NamibiaNAICSFactors.naics_id)),
    )


class NamibiaHSClassification(Base):
    __tablename__ = "hs_classification"
    __table_args__ = {"schema": "namibia"}

    hs_id = Column(Integer, primary_key=True)
    name = Column(String)
    code = Column(String)
    level = Column(String)
    parent_id = Column(Integer)
    complexity_report = Column(Boolean)
    in_tool = Column(Boolean)

    factors = relationship(
        "NamibiaHSFactors", primaryjoin=(hs_id == foreign(NamibiaHSFactors.hs_id))
    )
    relative_demand = relationship(
        "NamibiaHSRelativeDemand",
        primaryjoin=(hs_id == foreign(NamibiaHSRelativeDemand.hs_id)),
    )
    proximity = relationship(
        "NamibiaHSProximity", primaryjoin=(hs_id == foreign(NamibiaHSProximity.hs_id))
    )
    occupation = relationship(
        "NamibiaHSOccupation", primaryjoin=(hs_id == foreign(NamibiaHSOccupation.hs_id))
    )


class NamibiaNAICSClassification(Base):
    __tablename__ = "naics_classification"
    __table_args__ = {"schema": "namibia"}

    naics_id = Column(Integer, primary_key=True)
    name = Column(String)
    code = Column(Integer)
    level = Column(String)
    parent_id = Column(Integer)
    complexity_report = Column(Boolean)
    in_tool = Column(Boolean)

    factors = relationship(
        "NamibiaNAICSFactors",
        primaryjoin=(naics_id == foreign(NamibiaNAICSFactors.naics_id)),
    )
    relative_demand = relationship(
        "NamibiaNAICSRelativeDemand",
        primaryjoin=(naics_id == foreign(NamibiaNAICSRelativeDemand.naics_id)),
    )
    proximity = relationship(
        "NamibiaNAICSProximity",
        primaryjoin=(naics_id == foreign(NamibiaNAICSProximity.naics_id)),
    )
    occupation = relationship(
        "NamibiaNAICSOccupation",
        primaryjoin=(naics_id == foreign(NamibiaNAICSOccupation.naics_id)),
    )


class NamibiaThreshold(Base):
    __tablename__ = "threshold"
    __table_args__ = {"schema": "namibia"}

    key = Column(String, primary_key=True)
    value = Column(Float)
