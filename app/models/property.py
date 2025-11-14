"""Property-related models."""
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.resource import Resource


class PropertyType(SQLModel, table=True):
    """Stores complex/nested type definitions.
    
    Property types can be resource-specific (resource_id set) or global/shared (resource_id NULL).
    Examples: 
    - Resource-specific: AWS::S3::Bucket.LifecycleConfiguration
    - Global/shared: Tag (used by 438+ resources)
    """
    __tablename__ = "property_types"

    id: Optional[int] = Field(default=None, primary_key=True)
    resource_id: Optional[int] = Field(default=None, foreign_key="resources.id", index=True)
    type_name: str = Field(max_length=150, unique=True, nullable=False, index=True)
    documentation_url: Optional[str] = None

    # Relationships
    resource: Optional["Resource"] = Relationship(back_populates="property_types")
    properties: List["Property"] = Relationship(
        back_populates="property_type",
        sa_relationship_kwargs={"foreign_keys": "Property.property_type_id"}
    )


class Property(SQLModel, table=True):
    """Unified table storing properties for both resources AND property types.
    
    A property belongs to either a resource OR a property_type (polymorphic relationship).
    
    Constraints:
    - Must belong to EITHER a resource OR a property_type (not both, not neither)
    - Cannot be both list and map
    - Must have exactly one type specified (primitive OR complex)
    """
    __tablename__ = "properties"

    id: Optional[int] = Field(default=None, primary_key=True)
    resource_id: Optional[int] = Field(default=None, foreign_key="resources.id", index=True)
    property_type_id: Optional[int] = Field(default=None, foreign_key="property_types.id", index=True)
    property_name: str = Field(max_length=100, nullable=False)
    documentation_url: Optional[str] = None
    update_type: Optional[str] = Field(default=None, max_length=20)  # Mutable, Immutable, or Conditional
    is_required: bool = Field(default=False)
    is_list: bool = Field(default=False)
    is_map: bool = Field(default=False)
    primitive_type: Optional[str] = Field(default=None, max_length=30)  # String, Boolean, Integer, Double, Long, Json
    complex_type_id: Optional[int] = Field(default=None, foreign_key="property_types.id", index=True)
    list_allows_duplicates: Optional[bool] = None

    # Relationships
    resource: Optional["Resource"] = Relationship(
        back_populates="properties",
        sa_relationship_kwargs={"foreign_keys": "Property.resource_id"}
    )
    property_type: Optional["PropertyType"] = Relationship(
        back_populates="properties",
        sa_relationship_kwargs={"foreign_keys": "Property.property_type_id"}
    )
    complex_type: Optional["PropertyType"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "Property.complex_type_id"}
    )

