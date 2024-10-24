import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from sqlalchemy.orm import scoped_session, sessionmaker

from database.base import db_session
from database import green_growth as green_growth_db

from .util import sqlalchemy_filter


class GGSupplyChainProductMember(SQLAlchemyObjectType):
    class Meta:
        model = green_growth_db.GGSupplyChainProductMember
        interfaces = (graphene.relay.Node,)


class GGCountryProductYear(SQLAlchemyObjectType):
    class Meta:
        model = green_growth_db.GGCountryProductYear
        interfaces = (graphene.relay.Node,)


class GGCountryProductYearSupplyChain(SQLAlchemyObjectType):
    class Meta:
        model = green_growth_db.GGCountryProductYearSupplyChain
        interfaces = (graphene.relay.Node,)


class GGSupplyChain(SQLAlchemyObjectType):
    class Meta:
        model = green_growth_db.GGSupplyChain
        interfaces = (graphene.relay.Node,)


class GGLocationCountry(SQLAlchemyObjectType):
    class Meta:
        model = green_growth_db.GGLocationCountry
        interfaces = (graphene.relay.Node,)


class GGProduct(SQLAlchemyObjectType):
    class Meta:
        model = green_growth_db.GGProduct
        interfaces = (graphene.relay.Node,)


class GreenGrowthQuery(graphene.ObjectType):
    gg_product_list = graphene.List(GGProduct)
    gg_location_country_list = graphene.List(GGLocationCountry)
    gg_supply_chain_list = graphene.List(GGSupplyChain)
    gg_supply_chain_product_member_list = graphene.List(GGSupplyChainProductMember)
    gg_cpy_list = graphene.List(
        GGCountryProductYear,
        year=graphene.Int(required=True),
        country_id=graphene.Int(required=True),
    )
    gg_cpysc_list = graphene.List(
        GGCountryProductYearSupplyChain,
        year=graphene.Int(required=True),
        country_id=graphene.Int(required=True),
    )

    def resolve_gg_cpy_list(self, info, year, country_id):
        return (
            db_session.query(green_growth_db.GGCountryProductYear)
            .filter(green_growth_db.GGCountryProductYear.year == year)
            .filter(green_growth_db.GGCountryProductYear.country_id == country_id)
        )

    def resolve_gg_cpysc_list(self, info, year, country_id):
        return (
            db_session.query(green_growth_db.GGCountryProductYearSupplyChain)
            .filter(green_growth_db.GGCountryProductYearSupplyChain.year == year)
            .filter(
                green_growth_db.GGCountryProductYearSupplyChain.country_id == country_id
            )
        )

    def resolve_gg_product_list(self, info, **args):
        return db_session.query(green_growth_db.GGProduct)

    def resolve_gg_location_country_list(self, info, **args):
        return db_session.query(green_growth_db.GGLocationCountry)

    def resolve_gg_supply_chain_list(self, info, **args):
        return db_session.query(green_growth_db.GGSupplyChain)

    def resolve_gg_supply_chain_product_member_list(self, info, **args):
        return db_session.query(green_growth_db.GGSupplyChainProductMember)
