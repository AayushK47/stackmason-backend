"""Resource-related models."""
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.region import Region
    from app.models.property import Property, PropertyType


class Resource(SQLModel, table=True):
    """Stores CloudFormation resource types (deduplicated across regions)."""
    __tablename__ = "resources"

    id: Optional[int] = Field(default=None, primary_key=True)
    resource_type: str = Field(max_length=100, unique=True, nullable=False, index=True)
    documentation_url: Optional[str] = None
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    # Relationships
    resource_regions: List["ResourceRegion"] = Relationship(back_populates="resource")
    property_types: List["PropertyType"] = Relationship(back_populates="resource")
    properties: List["Property"] = Relationship(
        back_populates="resource",
        sa_relationship_kwargs={"foreign_keys": "Property.resource_id"}
    )
    attributes: List["ResourceAttribute"] = Relationship(back_populates="resource")


class ResourceRegion(SQLModel, table=True):
    """Many-to-many relationship: which resources are available in which regions."""
    __tablename__ = "resource_regions"

    id: Optional[int] = Field(default=None, primary_key=True)
    resource_id: int = Field(foreign_key="resources.id", nullable=False, index=True)
    region_id: int = Field(foreign_key="regions.id", nullable=False, index=True)

    # Relationships
    resource: Optional["Resource"] = Relationship(back_populates="resource_regions")
    region: Optional["Region"] = Relationship(back_populates="resource_regions")


class ResourceAttribute(SQLModel, table=True):
    """Stores return values (Fn::GetAtt) for CloudFormation resources.
    
    Attributes are simpler than properties - only primitives or lists of primitives.
    
    Constraint:
    - If not a list, must have primitive_type
    - If is a list, must have list_item_type
    """
    __tablename__ = "resource_attributes"

    id: Optional[int] = Field(default=None, primary_key=True)
    resource_id: int = Field(foreign_key="resources.id", nullable=False, index=True)
    attribute_name: str = Field(max_length=100, nullable=False)
    primitive_type: Optional[str] = Field(default=None, max_length=30)  # String, Integer, Boolean, etc.
    is_list: bool = Field(default=False)
    list_item_type: Optional[str] = Field(default=None, max_length=30)  # Type of items in the list if is_list=TRUE

    # Relationships
    resource: Optional["Resource"] = Relationship(back_populates="attributes")

