import graphene

from country_tools.country_tools_api.schemas.albania import AlbaniaQuery

from country_tools.country_tools_api.schemas.jordan import JordanQuery
from country_tools.country_tools_api.schemas.namibia import NamibiaQuery
from country_tools.country_tools_api.schemas.hub import HubQuery
from country_tools.country_tools_api.schemas.greenplexity import GreenplexityQuery
from country_tools.country_tools_api.schemas.green_growth import GreenGrowthQuery


class Query(AlbaniaQuery, JordanQuery, NamibiaQuery, HubQuery, GreenplexityQuery, GreenGrowthQuery):
    """Query objects for GraphQL API."""


schema = graphene.Schema(query=Query)
