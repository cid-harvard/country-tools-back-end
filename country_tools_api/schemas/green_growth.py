import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from sqlalchemy.orm import scoped_session, sessionmaker

from database.base import db_session
from database import green_growth as green_growth_db

from .util import sqlalchemy_filter


class SupplyChainProductMember(SQLAlchemyObjectType):
    class Meta:
        model = green_growth_db.SupplyChainProductMember
        interfaces = (graphene.relay.Node,)


class CountryProductYear(SQLAlchemyObjectType):
    class Meta:
        model = green_growth_db.CountryProductYear
        interfaces = (graphene.relay.Node,)


class SupplyChain(SQLAlchemyObjectType):
    class Meta:
        model = green_growth_db.SupplyChain
        interfaces = (graphene.relay.Node,)


class LocationCountry(SQLAlchemyObjectType):
    class Meta:
        model = green_growth_db.LocationCountry
        interfaces = (graphene.relay.Node,)


class Product(SQLAlchemyObjectType):
    class Meta:
        model = green_growth_db.Product
        interfaces = (graphene.relay.Node,)


class GreenGrowthQuery(graphene.ObjectType):
    gg_product_list = graphene.List(Product)
    gg_country_list = graphene.List(LocationCountry)
    gg_supply_chain_list = graphene.List(SupplyChain)
    gg_supply_chain_product_member_list = graphene.List(SupplyChainProductMember)
    gg_cpy_list = graphene.List(CountryProductYear)
    

    def resolve_gg_cpy_list(self, info, **args):
        q = db_session.query(green_growth_db.CountryProductYear)

        return (
            db_session.query(green_growth_db.CountryProductYear)
            .filter(
                getattr(green_growth_db.CountryProductYear, "year") == args["year"]
            )
            .filter(getattr(green_growth_db.CountryProductYear, "country_id") == args["country_id"]
                   )
        )