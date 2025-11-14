"""Resource-related GraphQL queries."""
from typing import List, Optional
import strawberry
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from app.database import get_db
from app.models import (
    Resource as ResourceModel,
    ResourceRegion,
    Property as PropertyModel
)
from app.graphql.types import (
    ResourceSummary,
    ResourceDetail,
    ResourceAttribute,
    Region
)
from app.graphql.utils import build_property_tree


@strawberry.type
class ResourceQueries:
    """Resource query resolvers."""
    
    @strawberry.field
    def resources_by_region(self, region_id: int, info) -> List[ResourceSummary]:
        """Get all resources available in a specific region."""
        db: Session = next(get_db())
        try:
            # Join through resource_regions to get resources for the specified region
            statement = (
                select(ResourceModel)
                .join(ResourceRegion, ResourceModel.id == ResourceRegion.resource_id)
                .where(ResourceRegion.region_id == region_id)
                .order_by(ResourceModel.resource_type)
            )
            resources = db.exec(statement).all()
            
            return [
                ResourceSummary(
                    id=resource.id,
                    resource_type=resource.resource_type,
                    documentation_url=resource.documentation_url
                )
                for resource in resources
            ]
        finally:
            db.close()
    
    @strawberry.field
    def resource_detail(self, resource_id: int, info) -> Optional[ResourceDetail]:
        """Get complete resource details with all properties, nested structures, and attributes."""
        db: Session = next(get_db())
        try:
            # Get resource with eager loading
            statement = (
                select(ResourceModel)
                .where(ResourceModel.id == resource_id)
                .options(
                    selectinload(ResourceModel.properties),
                    selectinload(ResourceModel.attributes),
                    selectinload(ResourceModel.resource_regions).selectinload(ResourceRegion.region)
                )
            )
            resource = db.exec(statement).first()
            
            if not resource:
                return None
            
            # Build property tree (only root level properties of the resource)
            root_statement = (
                select(PropertyModel)
                .where(PropertyModel.resource_id == resource_id)
                .order_by(PropertyModel.property_name)
            )
            root_properties = db.exec(root_statement).all()
            
            properties = [
                build_property_tree(prop, db)
                for prop in root_properties
            ]
            
            # Get attributes
            attributes = [
                ResourceAttribute(
                    id=attr.id,
                    attribute_name=attr.attribute_name,
                    primitive_type=attr.primitive_type,
                    is_list=attr.is_list or False,
                    list_item_type=attr.list_item_type
                )
                for attr in resource.attributes
            ]
            
            # Get available regions
            available_regions = [
                Region(
                    id=rr.region.id,
                    region_code=rr.region.region_code,
                    region_name=rr.region.region_name
                )
                for rr in resource.resource_regions
            ]
            
            return ResourceDetail(
                id=resource.id,
                resource_type=resource.resource_type,
                documentation_url=resource.documentation_url,
                properties=properties,
                attributes=attributes,
                available_regions=available_regions
            )
        finally:
            db.close()
    
    @strawberry.field
    def search_resources(self, query: str, region_id: Optional[int] = None, info=None) -> List[ResourceSummary]:
        """Search resources by name/type, optionally filtered by region."""
        db: Session = next(get_db())
        try:
            statement = select(ResourceModel)
            
            # Filter by region if specified
            if region_id:
                statement = (
                    statement
                    .join(ResourceRegion, ResourceModel.id == ResourceRegion.resource_id)
                    .where(ResourceRegion.region_id == region_id)
                )
            
            # Search by resource type
            statement = (
                statement
                .where(ResourceModel.resource_type.ilike(f"%{query}%"))
                .order_by(ResourceModel.resource_type)
                .limit(50)
            )
            resources = db.exec(statement).all()
            
            return [
                ResourceSummary(
                    id=resource.id,
                    resource_type=resource.resource_type,
                    documentation_url=resource.documentation_url
                )
                for resource in resources
            ]
        finally:
            db.close()

