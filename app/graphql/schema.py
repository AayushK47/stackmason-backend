"""Main GraphQL schema combining all queries."""
from typing import List, Optional
import strawberry
from app.graphql.types import (
    Region,
    ResourceSummary,
    ResourceDetail,
)
from app.graphql.queries import RegionQueries, ResourceQueries


@strawberry.type
class Query(RegionQueries, ResourceQueries):
    """Root query combining all domain queries."""
    pass


schema = strawberry.Schema(query=Query)

