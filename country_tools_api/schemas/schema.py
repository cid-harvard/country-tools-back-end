import graphene

from .albania import AlbaniaQuery
from .jordan import JordanQuery
from .namibia import NamibiaQuery
from .hub import HubQuery
from .green_growth import GreenGrowthQuery


class Query(AlbaniaQuery, JordanQuery, NamibiaQuery, HubQuery, GreenGrowthQuery):
    """Query objects for GraphQL API."""


schema = graphene.Schema(query=Query)
