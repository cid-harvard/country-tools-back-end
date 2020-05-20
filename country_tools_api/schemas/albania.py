import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from sqlalchemy.orm import scoped_session, sessionmaker

from database.base import db_session
from database import albania as albania_db, jordan as jordan_db

from .util import sqlalchemy_filter


# NACE Industry
class AlbaniaNACEIndustry(SQLAlchemyObjectType):
    class Meta:
        model = albania_db.AlbaniaNACEIndustry
        interfaces = (graphene.relay.Node,)


# Country
class AlbaniaCountry(SQLAlchemyObjectType):
    class Meta:
        model = albania_db.AlbaniaCountry
        interfaces = (graphene.relay.Node,)


# FDI Markets
class AlbaniaFDIMarkets(SQLAlchemyObjectType):
    class Meta:
        model = albania_db.AlbaniaFDIMarkets
        interfaces = (graphene.relay.Node,)


# FDI Markets Overtime
class AlbaniaFDIMarketsOvertime(SQLAlchemyObjectType):
    class Meta:
        model = albania_db.AlbaniaFDIMarketsOvertime
        interfaces = (graphene.relay.Node,)

    # Graphene can't handle enum options starting with non-alpha characters
    destination = graphene.String()


# Viability
class AlbaniaFactors(SQLAlchemyObjectType):
    class Meta:
        model = albania_db.AlbaniaFactors
        interfaces = (graphene.relay.Node,)

    # Graphene can't handle enum options starting with non-alpha characters
    rca = graphene.String()


# Script
class AlbaniaScript(SQLAlchemyObjectType):
    class Meta:
        model = albania_db.AlbaniaScript
        interfaces = (graphene.relay.Node,)


# Industry Now Location
class AlbaniaIndustryNowLocation(SQLAlchemyObjectType):
    class Meta:
        model = albania_db.AlbaniaIndustryNowLocation
        interfaces = (graphene.relay.Node,)


# Industry Now Schooling
class AlbaniaIndustryNowSchooling(SQLAlchemyObjectType):
    class Meta:
        model = albania_db.AlbaniaIndustryNowSchooling
        interfaces = (graphene.relay.Node,)


# Industry Now Occupation
class AlbaniaIndustryNowOccupation(SQLAlchemyObjectType):
    class Meta:
        model = albania_db.AlbaniaIndustryNowOccupation
        interfaces = (graphene.relay.Node,)


# Industry Now Wage
class AlbaniaIndustryNowWage(SQLAlchemyObjectType):
    class Meta:
        model = albania_db.AlbaniaIndustryNowWage
        interfaces = (graphene.relay.Node,)


# Industry Now Nearest Industry
class AlbaniaIndustryNowNearestIndustry(SQLAlchemyObjectType):
    class Meta:
        model = albania_db.AlbaniaIndustryNowNearestIndustry
        interfaces = (graphene.relay.Node,)


class AlbaniaQuery(graphene.ObjectType):
    """Albania query objects for GraphQL API."""

    # New endpoints
    albania_nace_industry_list = graphene.List(AlbaniaNACEIndustry)
    albania_nace_industry = graphene.Field(
        AlbaniaNACEIndustry, nace_id=graphene.Int(required=True)
    )

    # Old endpoints
    nace_industry_list = graphene.List(AlbaniaNACEIndustry)
    nace_industry = graphene.Field(
        AlbaniaNACEIndustry, nace_id=graphene.Int(required=True)
    )
    country = graphene.List(AlbaniaCountry, location_id=graphene.Int())
    fdi_markets = graphene.List(AlbaniaFDIMarkets, nace_id=graphene.Int())
    protected_fdi_markets = graphene.List(
        AlbaniaFDIMarkets, nace_id=graphene.Int(), key=graphene.String(required=True)
    )
    fdi_markets_overtime = graphene.List(
        AlbaniaFDIMarketsOvertime, nace_id=graphene.Int()
    )
    factors = graphene.List(AlbaniaFactors, nace_id=graphene.Int())
    script = graphene.List(AlbaniaScript)

    def resolve_albania_nace_industry_list(self, info, **args):
        return db_session.query(albania_db.AlbaniaNACEIndustry)

    def resolve_albania_nace_industry(self, info, **args):
        return (
            db_session.query(albania_db.AlbaniaNACEIndustry)
            .filter(
                getattr(albania_db.AlbaniaNACEIndustry, "nace_id") == args["nace_id"]
            )
            .one()
        )

    def resolve_nace_industry_list(self, info, **args):
        return db_session.query(albania_db.AlbaniaNACEIndustry)

    def resolve_nace_industry(self, info, **args):
        return (
            db_session.query(albania_db.AlbaniaNACEIndustry)
            .filter(
                getattr(albania_db.AlbaniaNACEIndustry, "nace_id") == args["nace_id"]
            )
            .one()
        )

    def resolve_country(self, info, **args):
        return sqlalchemy_filter(args, albania_db.AlbaniaCountry, "location_id")

    def resolve_fdi_markets(self, info, **args):
        return sqlalchemy_filter(args, albania_db.AlbaniaFDIMarkets, "nace_id")

    def resolve_protected_fdi_markets(self, info, **args):
        if args["key"] != "albania2020":
            return None
        return sqlalchemy_filter(args, albania_db.AlbaniaFDIMarkets, "nace_id")

    def resolve_fdi_markets_overtime(self, info, **args):
        return sqlalchemy_filter(args, albania_db.AlbaniaFDIMarketsOvertime, "nace_id")

    def resolve_factors(self, info, **args):
        return sqlalchemy_filter(args, albania_db.AlbaniaFactors, "nace_id")

    def resolve_script(self, info, **args):
        return db_session.query(albania_db.AlbaniaScript)
