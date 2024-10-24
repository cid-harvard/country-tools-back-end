import graphene

# from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from sqlalchemy.orm import scoped_session, sessionmaker

from country_tools.country_tools_api.database.base import db_session
from country_tools.country_tools_api.database import namibia as namibia_db

from country_tools.country_tools_api.schemas.util import sqlalchemy_filter


class NamibiaHSClassification(graphene.ObjectType):
    class Meta:
        model = namibia_db.NamibiaHSClassification
        interfaces = (graphene.relay.Node,)


class NamibiaNAICSClassification(graphene.ObjectType):
    class Meta:
        model = namibia_db.NamibiaNAICSClassification
        interfaces = (graphene.relay.Node,)


class NamibiaHSFactors(graphene.ObjectType):
    class Meta:
        model = namibia_db.NamibiaHSFactors
        interfaces = (graphene.relay.Node,)


class NamibiaNAICSFactors(graphene.ObjectType):
    class Meta:
        model = namibia_db.NamibiaNAICSFactors
        interfaces = (graphene.relay.Node,)


class NamibiaHSProximity(graphene.ObjectType):
    class Meta:
        model = namibia_db.NamibiaHSProximity
        interfaces = (graphene.relay.Node,)


class NamibiaNAICSProximity(graphene.ObjectType):
    class Meta:
        model = namibia_db.NamibiaNAICSProximity
        interfaces = (graphene.relay.Node,)


class NamibiaHSRelativeDemand(graphene.ObjectType):
    class Meta:
        model = namibia_db.NamibiaHSRelativeDemand
        interfaces = (graphene.relay.Node,)


class NamibiaNAICSRelativeDemand(graphene.ObjectType):
    class Meta:
        model = namibia_db.NamibiaNAICSRelativeDemand
        interfaces = (graphene.relay.Node,)


class NamibiaHSOccupation(graphene.ObjectType):
    class Meta:
        model = namibia_db.NamibiaHSOccupation
        interfaces = (graphene.relay.Node,)


class NamibiaNAICSOccupation(graphene.ObjectType):
    class Meta:
        model = namibia_db.NamibiaNAICSOccupation
        interfaces = (graphene.relay.Node,)


class NamibiaThreshold(graphene.ObjectType):
    class Meta:
        model = namibia_db.NamibiaThreshold
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

    namibia_threshold = graphene.Field(
        NamibiaThreshold, key=graphene.String(required=True)
    )
    namibia_threshold_list = graphene.List(NamibiaThreshold)

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

    def resolve_namibia_threshold(self, info, **args):
        return db_session.query(namibia_db.NamibiaThreshold).filter(
            getattr(namibia_db.NamibiaThreshold, "key") == args["key"]
        )

    def resolve_namibia_threshold_list(self, info, **args):
        return db_session.query(namibia_db.NamibiaThreshold)