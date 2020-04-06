from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
import graphene

from database.albania import *

# NACE Industry
class NACEIndustryAttribute:
    nace_id = graphene.String()
    level = graphene.String()
    code = graphene.String()
    name = graphene.String()
    parent_id = graphene.String()


class NACEIndustry(SQLAlchemyObjectType, NACEIndustryAttribute):
    class Meta:
        model = NACEIndustry
        interfaces = (graphene.relay.Node,)


# Country
class CountryAttribute:
    location_id = graphene.String()
    code = graphene.String()
    level = graphene.String()
    name_en = graphene.String()
    name_short_en = graphene.String()
    iso2 = graphene.String()
    parent_id = graphene.String()
    name = graphene.String()
    is_trusted = graphene.String()
    in_rankings = graphene.String()
    reported_serv = graphene.String()
    reported_serv_recent = graphene.String()
    former_country = graphene.String()


class Country(SQLAlchemyObjectType, CountryAttribute):
    class Meta:
        model = Country
        interfaces = (graphene.relay.Node,)


# FDI Markets
class FDIMarketsAttribute:
    nace_id = graphene.String()
    location_id = graphene.String()
    parent_company = graphene.String()
    source_country = graphene.String()
    source_city = graphene.String()
    capex_world = graphene.String()
    capex_europe = graphene.String()
    capex_balkans = graphene.String()
    projects_world = graphene.String()
    projects_europe = graphene.String()
    projects_balkans = graphene.String()


class FDIMarkets(SQLAlchemyObjectType, FDIMarketsAttribute):
    class Meta:
        model = FDIMarkets
        interfaces = (graphene.relay.Node,)


# FDI Markets Overtime
class FDIMarketsOvertimeAttribute:
    nace_id = graphene.String()
    destination = graphene.String()
    projects_03_06 = graphene.String()
    projects_07_10 = graphene.String()
    projects_11_14 = graphene.String()
    projects_15_18 = graphene.String()


class FDIMarketsOvertime(SQLAlchemyObjectType, FDIMarketsOvertimeAttribute):
    class Meta:
        model = FDIMarketsOvertime
        interfaces = (graphene.relay.Node,)


# Viability
class ViabilityAttribute:
    nace_id = graphene.String()
    score_rca = graphene.String()
    score_dist = graphene.String()
    score_fdipeers = graphene.String()
    score_contracts = graphene.String()


class Viability(SQLAlchemyObjectType, ViabilityAttribute):
    class Meta:
        model = Viability
        interfaces = (graphene.relay.Node,)


class Query(graphene.ObjectType):
    """Query objects for GraphQL API."""

    node = graphene.relay.Node.Field()
    nace_industry = graphene.relay.Node.Field(NACEIndustry)
    nace_industry_list = SQLAlchemyConnectionField(NACEIndustry)


schema = graphene.Schema(query=Query)
