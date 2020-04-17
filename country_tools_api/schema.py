import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from sqlalchemy.orm import scoped_session, sessionmaker

from database.base import db_session
from database import albania

# NACE Industry
class NACEIndustryAttribute:
    nace_id = graphene.String()
    level = graphene.String()
    code = graphene.String()
    name = graphene.String()
    parent_id = graphene.String()


class NACEIndustry(SQLAlchemyObjectType, NACEIndustryAttribute):
    class Meta:
        model = albania.NACEIndustry
        interfaces = (graphene.relay.Node,)


# Country
class CountryAttribute:
    location_id = graphene.Int()
    code = graphene.String()
    level = graphene.String()
    name_en = graphene.String()
    name_short_en = graphene.String()
    iso2 = graphene.String()
    parent_id = graphene.String()
    name = graphene.String()
    is_trusted = graphene.Boolean()
    in_rankings = graphene.Boolean()
    reported_serv = graphene.Boolean()
    reported_serv_recent = graphene.Boolean()
    former_country = graphene.Boolean()


class Country(SQLAlchemyObjectType, CountryAttribute):
    class Meta:
        model = albania.Country
        interfaces = (graphene.relay.Node,)


# FDI Markets
class FDIMarketsAttribute:
    nace_id = graphene.String()
    location_id = graphene.Int()
    parent_company = graphene.String()
    source_country = graphene.String()
    source_city = graphene.String()
    capex_world = graphene.Float()
    capex_europe = graphene.Float()
    capex_balkans = graphene.Float()
    projects_world = graphene.Int()
    projects_europe = graphene.Int()
    projects_balkans = graphene.Int()


class FDIMarkets(SQLAlchemyObjectType, FDIMarketsAttribute):
    class Meta:
        model = albania.FDIMarkets
        interfaces = (graphene.relay.Node,)


# FDI Markets Overtime
class FDIMarketsOvertimeAttribute:
    nace_id = graphene.String()
    destination = graphene.String()
    projects_03_06 = graphene.Int()
    projects_07_10 = graphene.Int()
    projects_11_14 = graphene.Int()
    projects_15_18 = graphene.Int()


class FDIMarketsOvertime(SQLAlchemyObjectType, FDIMarketsOvertimeAttribute):
    class Meta:
        model = albania.FDIMarketsOvertime
        interfaces = (graphene.relay.Node,)


# Viability
class FactorsAttribute:
    nace_id = graphene.String()
    rca = graphene.String()
    v_rca = graphene.Int()
    v_dist = graphene.Int()
    v_fdipeers = graphene.Int()
    v_contracts = graphene.Int()
    v_elect = graphene.Int()
    avg_viability = graphene.Float()
    a_youth = graphene.Int()
    a_wage = graphene.Int()
    a_fdiworld = graphene.Int()
    a_export = graphene.Int()
    avg_attractiveness = graphene.Float()
    v_text = graphene.String()
    a_text = graphene.String()
    rca_text1 = graphene.String()
    rca_text2 = graphene.String()


class Factors(SQLAlchemyObjectType, FactorsAttribute):
    class Meta:
        model = albania.Factors
        interfaces = (graphene.relay.Node,)


class Script(SQLAlchemyObjectType):
    class Meta:
        model = albania.Script
        interfaces = (graphene.relay.Node,)


class Query(graphene.ObjectType):
    """Query objects for GraphQL API."""

    nace_industry = graphene.List(NACEIndustry, nace_id=graphene.Int())
    country = graphene.List(Country, location_id=graphene.Int())
    fdi_markets = graphene.List(FDIMarkets, nace_id=graphene.Int())
    fdi_markets_overtime = graphene.List(FDIMarketsOvertime, nace_id=graphene.Int())
    factors = graphene.List(Factors, nace_id=graphene.Int())
    script = graphene.List(Script)

    def resolve_nace_industry(self, info, **args):
        query = db_session.query(albania.NACEIndustry).filter(
            getattr(albania.NACEIndustry, "nace_id") == args["nace_id"]
        )
        return query

    def resolve_country(self, info, **args):
        query = db_session.query(albania.Country).filter(
            getattr(albania.Country, "location_id") == args["location_id"]
        )
        return query

    def resolve_fdi_markets(self, info, **args):
        query = db_session.query(albania.FDIMarkets).filter(
            getattr(albania.FDIMarkets, "nace_id") == args["nace_id"]
        )
        return query

    def resolve_fdi_markets_overtime(self, info, **args):
        query = db_session.query(albania.FDIMarketsOvertime).filter(
            getattr(albania.FDIMarketsOvertime, "nace_id") == args["nace_id"]
        )
        return query

    def resolve_factors(self, info, **args):
        query = db_session.query(albania.Factors).filter(
            getattr(albania.Factors, "nace_id") == args["nace_id"]
        )
        return query


schema = graphene.Schema(query=Query)
