import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from sqlalchemy.orm import scoped_session, sessionmaker

from database.base import db_session
from database import albania

# NACE Industry
class NACEIndustry(SQLAlchemyObjectType):
    class Meta:
        model = albania.NACEIndustry
        interfaces = (graphene.relay.Node,)


# Country
class Country(SQLAlchemyObjectType):
    class Meta:
        model = albania.Country
        interfaces = (graphene.relay.Node,)


# FDI Markets
class FDIMarkets(SQLAlchemyObjectType):
    class Meta:
        model = albania.FDIMarkets
        interfaces = (graphene.relay.Node,)


# FDI Markets Overtime
class FDIMarketsOvertime(SQLAlchemyObjectType):
    class Meta:
        model = albania.FDIMarketsOvertime
        interfaces = (graphene.relay.Node,)

    # Graphene can't handle enum options starting with non-alpha characters
    destination = graphene.String()


# Viability
class Factors(SQLAlchemyObjectType):
    class Meta:
        model = albania.Factors
        interfaces = (graphene.relay.Node,)

    # Graphene can't handle enum options starting with non-alpha characters
    rca = graphene.String()


# Script
class Script(SQLAlchemyObjectType):
    class Meta:
        model = albania.Script
        interfaces = (graphene.relay.Node,)


# Industry Now Location
class IndustryNowLocation(SQLAlchemyObjectType):
    class Meta:
        model = albania.IndustryNowLocation
        interfaces = (graphene.relay.Node,)


# Industry Now Schooling
class IndustryNowSchooling(SQLAlchemyObjectType):
    class Meta:
        model = albania.IndustryNowSchooling
        interfaces = (graphene.relay.Node,)


# Industry Now Occupation
class IndustryNowOccupation(SQLAlchemyObjectType):
    class Meta:
        model = albania.IndustryNowOccupation
        interfaces = (graphene.relay.Node,)


# Industry Now Wage
class IndustryNowWage(SQLAlchemyObjectType):
    class Meta:
        model = albania.IndustryNowWage
        interfaces = (graphene.relay.Node,)


# Industry Now Nearest Industry
class IndustryNowNearestIndustry(SQLAlchemyObjectType):
    class Meta:
        model = albania.IndustryNowNearestIndustry
        interfaces = (graphene.relay.Node,)


def sqlalchemy_filter(args, model, col):
    query = db_session.query(model)
    if col in args:
        query = query.filter(getattr(model, col) == args[col])
    return query


class Query(graphene.ObjectType):
    """Query objects for GraphQL API."""

    nace_industry_list = graphene.List(NACEIndustry)
    nace_industry = graphene.Field(NACEIndustry, nace_id=graphene.Int(required=True))
    country = graphene.List(Country, location_id=graphene.Int())
    fdi_markets = graphene.List(FDIMarkets, nace_id=graphene.Int())
    fdi_markets_overtime = graphene.List(FDIMarketsOvertime, nace_id=graphene.Int())
    factors = graphene.List(Factors, nace_id=graphene.Int())
    script = graphene.List(Script)

    def resolve_nace_industry_list(self, info, **args):
        return db_session.query(albania.NACEIndustry)

    def resolve_nace_industry(self, info, **args):
        return (
            db_session.query(albania.NACEIndustry)
            .filter(getattr(albania.NACEIndustry, "nace_id") == args["nace_id"])
            .one()
        )

    def resolve_country(self, info, **args):
        return sqlalchemy_filter(args, albania.Country, "location_id")

    def resolve_fdi_markets(self, info, **args):
        return sqlalchemy_filter(args, albania.FDIMarkets, "nace_id")

    def resolve_fdi_markets_overtime(self, info, **args):
        return sqlalchemy_filter(args, albania.FDIMarketsOvertime, "nace_id")

    def resolve_factors(self, info, **args):
        return sqlalchemy_filter(args, albania.Factors, "nace_id")

    def resolve_script(self, info, **args):
        return db_session.query(albania.Script)


schema = graphene.Schema(query=Query)
