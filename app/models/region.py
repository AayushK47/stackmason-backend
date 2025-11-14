"""Region model."""
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.resource import ResourceRegion


class Region(SQLModel, table=True):
    """Stores AWS regions where CloudFormation resources are available."""
    __tablename__ = "regions"

    id: Optional[int] = Field(default=None, primary_key=True)
    region_code: str = Field(max_length=30, unique=True, nullable=False, index=True)
    region_name: str = Field(max_length=100, nullable=False)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    # Relationships
    resource_regions: List["ResourceRegion"] = Relationship(back_populates="region")

