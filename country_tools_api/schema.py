from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
import graphene
from graphene import String, Int, Boolean, Float

from database import albania

# NACE Industry
class NACEIndustryAttribute:
    nace_id = String()
    level = String()
    code = String()
    name = String()
    parent_id = String()


class NACEIndustry(SQLAlchemyObjectType, NACEIndustryAttribute):
    class Meta:
        model = albania.NACEIndustry
        interfaces = (graphene.relay.Node,)


# Country
class CountryAttribute:
    location_id = Int()
    code = String()
    level = String()
    name_en = String()
    name_short_en = String()
    iso2 = String()
    parent_id = String()
    name = String()
    is_trusted = Boolean()
    in_rankings = Boolean()
    reported_serv = Boolean()
    reported_serv_recent = Boolean()
    former_country = Boolean()


class Country(SQLAlchemyObjectType, CountryAttribute):
    class Meta:
        model = albania.Country
        interfaces = (graphene.relay.Node,)


# FDI Markets
class FDIMarketsAttribute:
    nace_id = String()
    location_id = Int()
    parent_company = String()
    source_country = String()
    source_city = String()
    capex_world = Float()
    capex_europe = Float()
    capex_balkans = Float()
    projects_world = Int()
    projects_europe = Int()
    projects_balkans = Int()


class FDIMarkets(SQLAlchemyObjectType, FDIMarketsAttribute):
    class Meta:
        model = albania.FDIMarkets
        interfaces = (graphene.relay.Node,)


# FDI Markets Overtime
class FDIMarketsOvertimeAttribute:
    nace_id = String()
    destination = String()
    projects_03_06 = Int()
    projects_07_10 = Int()
    projects_11_14 = Int()
    projects_15_18 = Int()


class FDIMarketsOvertime(SQLAlchemyObjectType, FDIMarketsOvertimeAttribute):
    class Meta:
        model = albania.FDIMarketsOvertime
        interfaces = (graphene.relay.Node,)


# Viability
class FactorsAttribute:
    nace_id = String()
    rca = String()
    v_rca = Int()
    v_dist = Int()
    v_fdipeers = Int()
    v_contracts = Int()
    v_elect = Int()
    avg_viability = Float()
    a_youth = Int()
    a_wage = Int()
    a_fdiworld = Int()
    a_export = Int()
    avg_attractiveness = Float()
    v_text = String()
    a_text = String()
    rca_text1 = String()
    rca_text2 = String()


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

    node = graphene.relay.Node.Field()
    nace_industry = graphene.relay.Node.Field(NACEIndustry)
    nace_industry_list = SQLAlchemyConnectionField(NACEIndustry)
    country = graphene.relay.Node.Field(Country)
    country_list = SQLAlchemyConnectionField(Country)
    fdi_markets = graphene.relay.Node.Field(FDIMarkets)
    fdi_markets_list = SQLAlchemyConnectionField(FDIMarkets)
    fdi_markets_overtime = graphene.relay.Node.Field(FDIMarketsOvertime)
    fdi_markets_overtime_list = SQLAlchemyConnectionField(FDIMarketsOvertime)
    factors = graphene.relay.Node.Field(Factors)
    factors_list = SQLAlchemyConnectionField(Factors)
    script = SQLAlchemyConnectionField(Script)


schema = graphene.Schema(query=Query)
