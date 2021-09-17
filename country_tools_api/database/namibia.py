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
from sqlalchemy.orm import relationship, foreign


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
