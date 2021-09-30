import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from sqlalchemy.orm import scoped_session, sessionmaker

from database.base import db_session
from database import albania as albania_db, jordan as jordan_db

from .util import sqlalchemy_filter


class JordanIndustry(SQLAlchemyObjectType):
    class Meta:
        model = jordan_db.JordanIndustry
        interfaces = (graphene.relay.Node,)


class JordanNationality(SQLAlchemyObjectType):
    class Meta:
        model = jordan_db.JordanNationality
        interfaces = (graphene.relay.Node,)


class JordanControl(SQLAlchemyObjectType):
    class Meta:
        model = jordan_db.JordanControl
        interfaces = (graphene.relay.Node,)


class JordanText(SQLAlchemyObjectType):
    class Meta:
        model = jordan_db.JordanText
        interfaces = (graphene.relay.Node,)


class JordanOccupation(SQLAlchemyObjectType):
    class Meta:
        model = jordan_db.JordanOccupation
        interfaces = (graphene.relay.Node,)


class JordanSchooling(SQLAlchemyObjectType):
    class Meta:
        model = jordan_db.JordanSchooling
        interfaces = (graphene.relay.Node,)


class JordanWageHistogram(SQLAlchemyObjectType):
    class Meta:
        model = jordan_db.JordanWageHistogram
        interfaces = (graphene.relay.Node,)


class JordanMapLocation(SQLAlchemyObjectType):
    class Meta:
        model = jordan_db.JordanMapLocation
        interfaces = (graphene.relay.Node,)


class JordanFactors(SQLAlchemyObjectType):
    class Meta:
        model = jordan_db.JordanFactors
        interfaces = (graphene.relay.Node,)


class JordanOverTime(SQLAlchemyObjectType):
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
