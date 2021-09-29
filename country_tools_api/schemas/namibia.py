import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from sqlalchemy.orm import scoped_session, sessionmaker

from database.base import db_session
from database import namibia as namibia_db

from .util import sqlalchemy_filter


class NamibiaHSClassification(SQLAlchemyObjectType):
    class Meta:
        model = namibia_db.NamibiaHSClassification
        interfaces = (graphene.relay.Node,)


class NamibiaNAICSClassification(SQLAlchemyObjectType):
    class Meta:
        model = namibia_db.NamibiaNAICSClassification
        interfaces = (graphene.relay.Node,)


class NamibiaHSFactors(SQLAlchemyObjectType):
    class Meta:
        model = namibia_db.NamibiaHSFactors
        interfaces = (graphene.relay.Node,)


class NamibiaNAICSFactors(SQLAlchemyObjectType):
    class Meta:
        model = namibia_db.NamibiaNAICSFactors
        interfaces = (graphene.relay.Node,)


class NamibiaHSProximity(SQLAlchemyObjectType):
    class Meta:
        model = namibia_db.NamibiaHSProximity
        interfaces = (graphene.relay.Node,)


class NamibiaNAICSProximity(SQLAlchemyObjectType):
    class Meta:
        model = namibia_db.NamibiaNAICSProximity
        interfaces = (graphene.relay.Node,)


class NamibiaHSRelativeDemand(SQLAlchemyObjectType):
    class Meta:
        model = namibia_db.NamibiaHSRelativeDemand
        interfaces = (graphene.relay.Node,)


class NamibiaNAICSRelativeDemand(SQLAlchemyObjectType):
    class Meta:
        model = namibia_db.NamibiaNAICSRelativeDemand
        interfaces = (graphene.relay.Node,)


class NamibiaHSOccupation(SQLAlchemyObjectType):
    class Meta:
        model = namibia_db.NamibiaHSOccupation
        interfaces = (graphene.relay.Node,)


class NamibiaNAICSOccupation(SQLAlchemyObjectType):
    class Meta:
        model = namibia_db.NamibiaNAICSOccupation
        interfaces = (graphene.relay.Node,)


class NamibiaQuery(graphene.ObjectType):
    namibia_hs_list = graphene.List(
        NamibiaHSClassification,
        in_tool=graphene.Boolean(default_value=True),
        complexity_report=graphene.Boolean(),
    )
    namibia_hs = graphene.Field(
        NamibiaHSClassification, hs_id=graphene.Int(required=True)
    )

    namibia_naics_list = graphene.List(
        NamibiaNAICSClassification,
        in_tool=graphene.Boolean(default_value=True),
        complexity_report=graphene.Boolean(),
    )
    namibia_naics = graphene.Field(
        NamibiaNAICSClassification, naics_id=graphene.Int(required=True)
    )

    def resolve_namibia_hs_list(self, info, **args):
        q = db_session.query(namibia_db.NamibiaHSClassification)

        for flag in ("in_tool", "complexity_report"):
            if args.get(flag):
                q = q.filter(
                    getattr(namibia_db.NamibiaHSClassification, flag) == args[flag]
                )

        return q

    def resolve_namibia_hs(self, info, **args):
        return (
            db_session.query(namibia_db.NamibiaHSClassification)
            .filter(
                getattr(namibia_db.NamibiaHSClassification, "hs_id") == args["hs_id"]
            )
            .one()
        )

    def resolve_namibia_naics_list(self, info, **args):
        q = db_session.query(namibia_db.NamibiaNAICSClassification)

        for flag in ("in_tool", "complexity_report"):
            if args.get(flag):
                q = q.filter(
                    getattr(namibia_db.NamibiaNAICSClassification, flag) == args[flag]
                )

        return q

    def resolve_namibia_naics(self, info, **args):
        return (
            db_session.query(namibia_db.NamibiaNAICSClassification)
            .filter(
                getattr(namibia_db.NamibiaNAICSClassification, "naics_id")
                == args["naics_id"]
            )
            .one()
        )
