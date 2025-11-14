"""GraphQL types for resources."""
from typing import Optional, List
import strawberry
from app.graphql.types.region import Region
from app.graphql.types.property import PropertyDetail


@strawberry.type
class ResourceSummary:
    """Simplified resource information for listing."""
    id: int
    resource_type: str
    documentation_url: Optional[str]


@strawberry.type
class ResourceAttribute:
    """Return values (Fn::GetAtt) for CloudFormation resources."""
    id: int
    attribute_name: str
    primitive_type: Optional[str]
    is_list: bool
    list_item_type: Optional[str]


@strawberry.type
class ResourceDetail:
    """Complete resource information with all properties and nested structures."""
    id: int
    resource_type: str
    documentation_url: Optional[str]
    properties: List[PropertyDetail]
    attributes: List[ResourceAttribute]
    available_regions: List[Region]

