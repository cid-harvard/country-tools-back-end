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

    destination = graphene.String()


# Viability
class Factors(SQLAlchemyObjectType):
    class Meta:
        model = albania.Factors
        interfaces = (graphene.relay.Node,)

    rca = graphene.String()


# Script
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
        query = db_session.query(albania.NACEIndustry)
        if "nace_id" in args:
            query = query.filter(
                getattr(albania.NACEIndustry, "nace_id") == args["nace_id"]
            )
        return query

    def resolve_country(self, info, **args):
        query = db_session.query(albania.Country)
        if "location_id" in args:
            query = query.filter(
                getattr(albania.Country, "location_id") == args["location_id"]
            )
        return query

    def resolve_fdi_markets(self, info, **args):
        query = db_session.query(albania.FDIMarkets)
        if "nace_id" in args:
            query = query.filter(
                getattr(albania.FDIMarkets, "nace_id") == args["nace_id"]
            )
        return query

    def resolve_fdi_markets_overtime(self, info, **args):
        query = db_session.query(albania.FDIMarketsOvertime)
        if "nace_id" in args:
            query = query.filter(
                getattr(albania.FDIMarketsOvertime, "nace_id") == args["nace_id"]
            )
        return query

    def resolve_factors(self, info, **args):
        query = db_session.query(albania.Factors)
        if "nace_id" in args:
            query = query.filter(getattr(albania.Factors, "nace_id") == args["nace_id"])
        return query


schema = graphene.Schema(query=Query)
