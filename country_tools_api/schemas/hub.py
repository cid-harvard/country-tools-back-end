import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import func
from collections import Counter

from database.base import db_session
from database import hub as hub_db

from .util import sqlalchemy_filter


class HubProjects(SQLAlchemyObjectType):
    class Meta:
        model = hub_db.HubProjects
        interfaces = (graphene.relay.Node,)

    data = graphene.List(graphene.String)
    keywords = graphene.List(graphene.String)


class HubKeywords(graphene.ObjectType):
    keyword = graphene.String()
    projects = graphene.Int()


class HubQuery(graphene.ObjectType):
    """Hub query objects for GraphQL API."""

    hub_projects_list = graphene.List(HubProjects)
    hub_projects = graphene.Field(
        HubProjects, project_name=graphene.String(required=True)
    )
    hub_keywords_list = graphene.List(HubKeywords)

    def resolve_hub_projects_list(self, info, **args):
        return db_session.query(hub_db.HubProjects)

    def resolve_hub_projects(self, info, **args):
        return (
            db_session.query(hub_db.HubProjects)
            .filter(getattr(hub_db.HubProjects, "project_name") == args["project_name"])
            .one()
        )

    def resolve_hub_keywords_list(self, info, **args):
        keywords = []

        c = Counter(
            [
                x[0]
                for x in (
                    db_session.query(func.unnest(hub_db.HubProjects.keywords)).all()
                )
            ]
        )

        for key, count in c.items():
            keywords.append(HubKeywords(key, count))

        return keywords

