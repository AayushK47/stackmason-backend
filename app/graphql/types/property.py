"""GraphQL types for properties."""
from typing import Optional, List
import strawberry


@strawberry.type
class PropertyTypeInfo:
    """Information about a complex property type."""
    id: int
    type_name: str
    documentation_url: Optional[str]


@strawberry.type
class PropertyDetail:
    """Detailed property information with nested structure."""
    id: int
    property_name: str
    documentation_url: Optional[str]
    update_type: Optional[str]
    is_required: bool
    is_list: bool
    is_map: bool
    primitive_type: Optional[str]
    complex_type_id: Optional[int]
    complex_type_name: Optional[str]
    list_allows_duplicates: Optional[bool]
    
    # Nested properties if this is a complex type
    nested_properties: Optional[List["PropertyDetail"]] = None

