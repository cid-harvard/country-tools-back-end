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


class Country(Base):

    __tablename__ = "country"
    # __table_args__ = {"schema": "albania"}

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
        {}
        # {"schema": "albania"},
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
    avg_capex = Column(Float)
    avg_jobs = Column(Float)
    country = relationship(
        "Country", primaryjoin=(location_id == foreign(Country.location_id))
    )


class FDIMarketsOvertime(Base):

    __tablename__ = "fdi_markets_overtime"
    __table_args__ = (
        PrimaryKeyConstraint("nace_id", "destination"),
        {}
        # {"schema": "albania"},
    )

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
    # __table_args__ = {"schema": "albania"}

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


class IndustryNowLocation(Base):
    __tablename__ = "industry_now_location"
    # __table_args__ = {"schema": "albania"}

    nace_id = Column(Integer, primary_key=True)
    berat = Column(Float)
    diber = Column(Float)
    durres = Column(Float)
    elbasan = Column(Float)
    fier = Column(Float)
    gjirokaster = Column(Float)
    korce = Column(Float)
    kukes = Column(Float)
    lezhe = Column(Float)
    shkoder = Column(Float)
    tirane = Column(Float)
    vlore = Column(Float)


class IndustryNowSchooling(Base):
    __tablename__ = "industry_now_schooling"
    # __table_args__ = {"schema": "albania"}

    nace_id = Column(Integer, primary_key=True)
    es_below_male = Column(Float)
    es_below_female = Column(Float)
    lower_secondary_male = Column(Float)
    lower_secondary_female = Column(Float)
    technical_vocational_male = Column(Float)
    technical_vocational_female = Column(Float)
    hs_some_college_male = Column(Float)
    hs_some_college_female = Column(Float)
    university_higher_male = Column(Float)
    university_higher_female = Column(Float)


class IndustryNowOccupation(Base):
    __tablename__ = "industry_now_occupation"
    # __table_args__ = {"schema": "albania"}

    nace_id = Column(Integer, primary_key=True)
    managers_male = Column(Float)
    managers_female = Column(Float)
    professionals_male = Column(Float)
    professionals_female = Column(Float)
    technicians_male = Column(Float)
    technicians_female = Column(Float)
    clerical_male = Column(Float)
    clerical_female = Column(Float)
    services_male = Column(Float)
    services_female = Column(Float)
    craft_male = Column(Float)
    craft_female = Column(Float)
    assembly_male = Column(Float)
    assembly_female = Column(Float)
    primary_male = Column(Float)
    primary_female = Column(Float)
    elementary_male = Column(Float)
    elementary_female = Column(Float)
    other_male = Column(Float)
    other_female = Column(Float)


class IndustryNowWage(Base):
    __tablename__ = "industry_now_wage"
    # __table_args__ = {"schema": "albania"}

    nace_id = Column(Integer, primary_key=True)
    ind_0_10k = Column(Float)
    ind_10k_25k = Column(Float)
    ind_25k_50k = Column(Float)
    ind_50k_75k = Column(Float)
    ind_75k_100k = Column(Float)
    ind_100k_up = Column(Float)
    national_0_10k = Column(Float)
    national_10k_25k = Column(Float)
    national_25k_50k = Column(Float)
    national_50k_75k = Column(Float)
    national_75k_100k = Column(Float)
    national_100k_up = Column(Float)


class IndustryNowNearestIndustry(Base):
    __tablename__ = "industry_now_nearest_industry"
    __table_args__ = (
        PrimaryKeyConstraint("nace_id", "place"),
        {}
        # {"schema": "albania"}
    )

    nace_id = Column(Integer)
    place = Column(Integer)
    neighbor_nace_id = Column(Integer)
    neighbor_code = Column(String)
    neighbor_name = Column(String)
    neighbor_rca_gte1 = Column(Boolean)


class Script(Base):

    __tablename__ = "script"
    __table_args__ = (
        PrimaryKeyConstraint("section", "subsection"),
        {}
        # {"schema": "albania"},
    )

    section = Column(String)
    subsection = Column(String)
    text = Column(String)


class NACEIndustry(Base):

    __tablename__ = "nace_industry"
    # __table_args__ = {"schema": "albania"}

    nace_id = Column(Integer, primary_key=True)
    level = Column(Enum(*["section", "division", "group"], name="industry_level"))
    code = Column(String)
    name = Column(String)
    parent_id = Column(Integer)
    fdi_markets = relationship(
        "FDIMarkets", primaryjoin=(nace_id == foreign(FDIMarkets.nace_id))
    )
    fdi_markets_overtime = relationship(
        "FDIMarketsOvertime",
        primaryjoin=(nace_id == foreign(FDIMarketsOvertime.nace_id)),
    )
    factors = relationship("Factors", primaryjoin=(nace_id == foreign(Factors.nace_id)))
    industry_now_location = relationship(
        "IndustryNowLocation",
        primaryjoin=(nace_id == foreign(IndustryNowLocation.nace_id)),
    )
    industry_now_schooling = relationship(
        "IndustryNowSchooling",
        primaryjoin=(nace_id == foreign(IndustryNowSchooling.nace_id)),
    )
    industry_now_occupation = relationship(
        "IndustryNowOccupation",
        primaryjoin=(nace_id == foreign(IndustryNowOccupation.nace_id)),
    )
    industry_now_wage = relationship(
        "IndustryNowWage", primaryjoin=(nace_id == foreign(IndustryNowWage.nace_id))
    )
    industry_now_nearest_industry = relationship(
        "IndustryNowNearestIndustry",
        primaryjoin=(nace_id == foreign(IndustryNowNearestIndustry.nace_id)),
    )
