import graphene

from .albania import AlbaniaQuery
from .jordan import JordanQuery


class Query(AlbaniaQuery, JordanQuery):
    """Query objects for GraphQL API."""


schema = graphene.Schema(query=Query)
