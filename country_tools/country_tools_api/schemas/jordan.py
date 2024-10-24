import graphene

# from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from sqlalchemy.orm import scoped_session, sessionmaker

from country_tools.country_tools_api.database.base import db_session
from country_tools.country_tools_api.database import (
    albania as albania_db,
    jordan as jordan_db,
)

from country_tools.country_tools_api.schemas.util import sqlalchemy_filter


class JordanIndustry(graphene.ObjectType):
    class Meta:
        model = jordan_db.JordanIndustry
        interfaces = (graphene.relay.Node,)


class JordanNationality(graphene.ObjectType):
    class Meta:
        model = jordan_db.JordanNationality
        interfaces = (graphene.relay.Node,)


class JordanControl(graphene.ObjectType):
    class Meta:
        model = jordan_db.JordanControl
        interfaces = (graphene.relay.Node,)


class JordanText(graphene.ObjectType):
    class Meta:
        model = jordan_db.JordanText
        interfaces = (graphene.relay.Node,)


class JordanOccupation(graphene.ObjectType):
    class Meta:
        model = jordan_db.JordanOccupation
        interfaces = (graphene.relay.Node,)


class JordanSchooling(graphene.ObjectType):
    class Meta:
        model = jordan_db.JordanSchooling
        interfaces = (graphene.relay.Node,)


class JordanWageHistogram(graphene.ObjectType):
    class Meta:
        model = jordan_db.JordanWageHistogram
        interfaces = (graphene.relay.Node,)


class JordanMapLocation(graphene.ObjectType):
    class Meta:
        model = jordan_db.JordanMapLocation
        interfaces = (graphene.relay.Node,)


class JordanFactors(graphene.ObjectType):
    class Meta:
        model = jordan_db.JordanFactors
        interfaces = (graphene.relay.Node,)


class JordanOverTime(graphene.ObjectType):
    class Meta:
        model = jordan_db.JordanOverTime
        interfaces = (graphene.relay.Node,)


class JordanQuery(graphene.ObjectType):
    """Jordan query objects for GraphQL API."""

    jordan_industry_list = graphene.List(JordanIndustry)
    jordan_industry = graphene.Field(
        JordanIndustry, industry_code=graphene.Int(required=True)
    )

    def resolve_jordan_industry_list(self, info, **args):
        return db_session.query(jordan_db.JordanIndustry)

    def resolve_jordan_industry(self, info, **args):
        return (
            db_session.query(jordan_db.JordanIndustry)
            .filter(
                getattr(jordan_db.JordanIndustry, "industry_code")
                == args["industry_code"]
            )
            .one()
        )
