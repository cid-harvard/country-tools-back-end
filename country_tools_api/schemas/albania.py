import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from sqlalchemy.orm import scoped_session, sessionmaker

from database.base import db_session
from database import albania as albania_db, jordan as jordan_db

from .util import sqlalchemy_filter


# NACE Industry
class NACEIndustry(SQLAlchemyObjectType):
    class Meta:
        model = albania_db.NACEIndustry
        interfaces = (graphene.relay.Node,)


# Country
class Country(SQLAlchemyObjectType):
    class Meta:
        model = albania_db.Country
        interfaces = (graphene.relay.Node,)


# FDI Markets
class FDIMarkets(SQLAlchemyObjectType):
    class Meta:
        model = albania_db.FDIMarkets
        interfaces = (graphene.relay.Node,)


# FDI Markets Overtime
class FDIMarketsOvertime(SQLAlchemyObjectType):
    class Meta:
        model = albania_db.FDIMarketsOvertime
        interfaces = (graphene.relay.Node,)

    # Graphene can't handle enum options starting with non-alpha characters
    destination = graphene.String()


# Viability
class Factors(SQLAlchemyObjectType):
    class Meta:
        model = albania_db.Factors
        interfaces = (graphene.relay.Node,)

    # Graphene can't handle enum options starting with non-alpha characters
    rca = graphene.String()


# Script
class Script(SQLAlchemyObjectType):
    class Meta:
        model = albania_db.Script
        interfaces = (graphene.relay.Node,)


# Industry Now Location
class IndustryNowLocation(SQLAlchemyObjectType):
    class Meta:
        model = albania_db.IndustryNowLocation
        interfaces = (graphene.relay.Node,)


# Industry Now Schooling
class IndustryNowSchooling(SQLAlchemyObjectType):
    class Meta:
        model = albania_db.IndustryNowSchooling
        interfaces = (graphene.relay.Node,)


# Industry Now Occupation
class IndustryNowOccupation(SQLAlchemyObjectType):
    class Meta:
        model = albania_db.IndustryNowOccupation
        interfaces = (graphene.relay.Node,)


# Industry Now Wage
class IndustryNowWage(SQLAlchemyObjectType):
    class Meta:
        model = albania_db.IndustryNowWage
        interfaces = (graphene.relay.Node,)


# Industry Now Nearest Industry
class IndustryNowNearestIndustry(SQLAlchemyObjectType):
    class Meta:
        model = albania_db.IndustryNowNearestIndustry
        interfaces = (graphene.relay.Node,)


class AlbaniaQuery(graphene.ObjectType):
    """Albania query objects for GraphQL API."""

    # New endpoints
    albania_nace_industry_list = graphene.List(NACEIndustry)
    albania_nace_industry = graphene.Field(
        NACEIndustry, nace_id=graphene.Int(required=True)
    )

    # Old endpoints
    nace_industry_list = graphene.List(NACEIndustry)
    nace_industry = graphene.Field(NACEIndustry, nace_id=graphene.Int(required=True))
    country = graphene.List(Country, location_id=graphene.Int())
    fdi_markets = graphene.List(FDIMarkets, nace_id=graphene.Int())
    protected_fdi_markets = graphene.List(
        FDIMarkets, nace_id=graphene.Int(), key=graphene.String(required=True)
    )
    fdi_markets_overtime = graphene.List(FDIMarketsOvertime, nace_id=graphene.Int())
    factors = graphene.List(Factors, nace_id=graphene.Int())
    script = graphene.List(Script)

    def resolve_albania_nace_industry_list(self, info, **args):
        return db_session.query(albania_db.NACEIndustry)

    def resolve_albania_nace_industry(self, info, **args):
        return (
            db_session.query(albania_db.NACEIndustry)
            .filter(getattr(albania_db.NACEIndustry, "nace_id") == args["nace_id"])
            .one()
        )

    def resolve_nace_industry_list(self, info, **args):
        return db_session.query(albania_db.NACEIndustry)

    def resolve_nace_industry(self, info, **args):
        return (
            db_session.query(albania_db.NACEIndustry)
            .filter(getattr(albania_db.NACEIndustry, "nace_id") == args["nace_id"])
            .one()
        )

    def resolve_country(self, info, **args):
        return sqlalchemy_filter(args, albania_db.Country, "location_id")

    def resolve_fdi_markets(self, info, **args):
        return sqlalchemy_filter(args, albania_db.FDIMarkets, "nace_id")

    def resolve_protected_fdi_markets(self, info, **args):
        if args["key"] != "albania2020":
            return None
        return sqlalchemy_filter(args, albania_db.FDIMarkets, "nace_id")

    def resolve_fdi_markets_overtime(self, info, **args):
        return sqlalchemy_filter(args, albania_db.FDIMarketsOvertime, "nace_id")

    def resolve_factors(self, info, **args):
        return sqlalchemy_filter(args, albania_db.Factors, "nace_id")

    def resolve_script(self, info, **args):
        return db_session.query(albania_db.Script)
