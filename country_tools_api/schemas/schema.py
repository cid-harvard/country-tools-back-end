import graphene

from .albania import AlbaniaQuery
from .jordan import JordanQuery
from .namibia import NamibiaQuery
from .hub import HubQuery


class Query(AlbaniaQuery, JordanQuery, NamibiaQuery, HubQuery):
    """Query objects for GraphQL API."""


schema = graphene.Schema(query=Query)
