"""GraphQL types package."""
from app.graphql.types.region import Region
from app.graphql.types.resource import ResourceSummary, ResourceAttribute, ResourceDetail
from app.graphql.types.property import PropertyTypeInfo, PropertyDetail

__all__ = [
    "Region",
    "ResourceSummary",
    "ResourceAttribute",
    "ResourceDetail",
    "PropertyTypeInfo",
    "PropertyDetail",
]

