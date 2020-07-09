import graphene

from .albania import AlbaniaQuery
from .jordan import JordanQuery
from .hub import HubQuery


class Query(AlbaniaQuery, JordanQuery, HubQuery):
    """Query objects for GraphQL API."""


schema = graphene.Schema(query=Query)
