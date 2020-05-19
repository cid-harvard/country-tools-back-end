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


class JordanNationality(Base):

    __tablename__ = "nationality"
    __table_args__ = (
        PrimaryKeyConstraint("industry_code", "nationality"),
        {"schema": "jordan"},
    )

    industry_code = Column(Integer)
    nationality = Column(String)
    men = Column(String)
    women = Column(String)
    meanwage = Column(String)
    medianwage = Column(String)


class JordanControl(Base):

    __tablename__ = "control"
    __table_args__ = {"schema": "jordan"}

    industry_code = Column(Integer, primary_key=True)
    labor = Column(Integer)
    women = Column(Integer)
    fdi = Column(Integer)


class JordanText(Base):

    __tablename__ = "text"
    __table_args__ = {"schema": "jordan"}

    industry_code = Column(Integer, primary_key=True)
    occupation = Column(String)
    demographic = Column(String)
    location = Column(String)
    avg_wage = Column(String)
    wage_hist = Column(String)
    scatter = Column(String)
    schooling = Column(String)
    percent_female = Column(String)
    percent_high_skill = Column(String)
    female = Column(String)
    high_skill = Column(String)


class JordanOccupation(Base):

    __tablename__ = "occupation"
    __table_args__ = (
        PrimaryKeyConstraint("industry_code", "occupation"),
        {"schema": "jordan"},
    )

    industry_code = Column(Integer)
    occupation = Column(String)
    men = Column(String)
    women = Column(String)


class JordanSchooling(Base):

    __tablename__ = "schooling"
    __table_args__ = (
        PrimaryKeyConstraint("industry_code", "schooling"),
        {"schema": "jordan"},
    )

    industry_code = Column(Integer, primary_key=True)
    schooling = Column(String)
    men = Column(String)
    women = Column(String)


class JordanWageHistogram(Base):

    __tablename__ = "wage_histogram"
    __table_args__ = (
        PrimaryKeyConstraint("industry_code", "facet"),
        {"schema": "jordan"},
    )

    industry_code = Column(Integer)
    facet = Column(String)
    range_0_100 = Column(Integer)
    range_100_200 = Column(Integer)
    range_200_300 = Column(Integer)
    range_300_400 = Column(Integer)
    range_400_500 = Column(Integer)
    range_500_600 = Column(Integer)
    range_600_plus = Column(Integer)


class JordanMapLocation(Base):

    __tablename__ = "map_location"
    __table_args__ = (
        PrimaryKeyConstraint("industry_code", "gov_code"),
        {"schema": "jordan"},
    )

    industry_code = Column(Integer, primary_key=True)
    gov_code = Column(String)
    governorate = Column(String)
    share_state = Column(String)
    share_country = Column(String)


class JordanGlobalTopFDI(Base):

    __tablename__ = "global_top_fdi"
    __table_args__ = (
        PrimaryKeyConstraint("industry_code", "rank"),
        {"schema": "jordan"},
    )

    industry_code = Column(Integer)
    rank = Column(Integer)
    company = Column(String)
    source_country = Column(String)
    capital_investment = Column(Float)


class JordanRegionTopFDI(Base):

    __tablename__ = "region_top_fdi"
    __table_args__ = (
        PrimaryKeyConstraint("industry_code", "rank"),
        {"schema": "jordan"},
    )

    industry_code = Column(Integer)
    rank = Column(Integer)
    company = Column(String)
    source_country = Column(String)
    capital_investment = Column(Float)


class JordanFactors(Base):

    __tablename__ = "factors"
    __table_args__ = {"schema": "jordan"}

    industry_code = Column(Integer, primary_key=True)
    rca_jordan = Column(Float)
    rca_peers = Column(Float)
    water_intensity = Column(Float)
    electricity_intensity = Column(Float)
    availability_inputs = Column(Float)
    female_employment = Column(Float)
    high_skill_employment = Column(Float)
    fdi_world = Column(Float)
    fdi_region = Column(Float)
    export_propensity = Column(Float)
    viability = Column(Float)
    attractiveness = Column(Float)
    viability_median = Column(Integer)
    attractiveness_median = Column(Integer)
    category = Column(String)
    rca = Column(Float)


class JordanIndustry(Base):

    __tablename__ = "industry"
    __table_args__ = {"schema": "jordan"}

    industry_code = Column(Integer, primary_key=True)
    title = Column(String)
    theme = Column(String)
    subtheme = Column(String)
    description = Column(String)
    keywords = Column(String)

    control = relationship(
        "JordanControl",
        primaryjoin=(industry_code == foreign(JordanControl.industry_code)),
    )
    factors = relationship(
        "JordanFactors",
        primaryjoin=(industry_code == foreign(JordanFactors.industry_code)),
    )
    global_top_fdi = relationship(
        "JordanGlobalTopFDI",
        primaryjoin=(industry_code == foreign(JordanGlobalTopFDI.industry_code)),
    )
    map_location = relationship(
        "JordanMapLocation",
        primaryjoin=(industry_code == foreign(JordanMapLocation.industry_code)),
    )
    nationality = relationship(
        "JordanNationality",
        primaryjoin=(industry_code == foreign(JordanNationality.industry_code)),
    )
    occupation = relationship(
        "JordanOccupation",
        primaryjoin=(industry_code == foreign(JordanOccupation.industry_code)),
    )
    region_top_fdi = relationship(
        "JordanRegionTopFDI",
        primaryjoin=(industry_code == foreign(JordanRegionTopFDI.industry_code)),
    )
    schooling = relationship(
        "JordanSchooling",
        primaryjoin=(industry_code == foreign(JordanSchooling.industry_code)),
    )
    text = relationship(
        "JordanText", primaryjoin=(industry_code == foreign(JordanText.industry_code))
    )
    wage_histogram = relationship(
        "JordanWageHistogram",
        primaryjoin=(industry_code == foreign(JordanWageHistogram.industry_code)),
    )
