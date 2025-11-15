"""Resource-related GraphQL queries."""
from typing import List, Optional
import strawberry
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from sqlalchemy import func
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
    Region,
    PaginatedResources
)
from app.graphql.utils import build_property_tree


@strawberry.type
class ResourceQueries:
    """Resource query resolvers."""
    
    @strawberry.field
    def resources_by_region(
        self, 
        region_id: int, 
        limit: int = 50,
        offset: int = 0,
        info = None
    ) -> PaginatedResources:
        """Get resources available in a specific region with pagination.
        
        Args:
            region_id: ID of the AWS region
            limit: Number of resources per page (default: 50, max: 100)
            offset: Number of resources to skip (default: 0)
        """
        # Enforce max limit
        limit = min(limit, 100)
        
        db: Session = next(get_db())
        try:
            # Base query
            base_statement = (
                select(ResourceModel)
                .join(ResourceRegion, ResourceModel.id == ResourceRegion.resource_id)
                .where(ResourceRegion.region_id == region_id)
            )
            
            # Get total count
            count_statement = (
                select(func.count())
                .select_from(ResourceModel)
                .join(ResourceRegion, ResourceModel.id == ResourceRegion.resource_id)
                .where(ResourceRegion.region_id == region_id)
            )
            total = db.exec(count_statement).one()
            
            # Get paginated resources
            statement = (
                base_statement
                .order_by(ResourceModel.resource_type)
                .limit(limit)
                .offset(offset)
            )
            resources = db.exec(statement).all()
            
            return PaginatedResources(
                resources=[
                    ResourceSummary(
                        id=resource.id,
                        resource_type=resource.resource_type,
                        documentation_url=resource.documentation_url
                    )
                    for resource in resources
                ],
                total=total,
                limit=limit,
                offset=offset,
                has_more=(offset + limit) < total
            )
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
    def search_resources(
        self, 
        query: str, 
        region_id: Optional[int] = None,
        limit: int = 50,
        offset: int = 0,
        info=None
    ) -> PaginatedResources:
        """Search resources by name/type, optionally filtered by region.
        
        Args:
            query: Search term to match against resource types
            region_id: Optional region ID to filter by
            limit: Number of resources per page (default: 50, max: 100)
            offset: Number of resources to skip (default: 0)
        """
        # Enforce max limit
        limit = min(limit, 100)
        
        db: Session = next(get_db())
        try:
            base_statement = select(ResourceModel)
            count_base = select(func.count()).select_from(ResourceModel)
            
            # Filter by region if specified
            if region_id:
                base_statement = (
                    base_statement
                    .join(ResourceRegion, ResourceModel.id == ResourceRegion.resource_id)
                    .where(ResourceRegion.region_id == region_id)
                )
                count_base = (
                    count_base
                    .join(ResourceRegion, ResourceModel.id == ResourceRegion.resource_id)
                    .where(ResourceRegion.region_id == region_id)
                )
            
            # Apply search filter
            search_filter = ResourceModel.resource_type.ilike(f"%{query}%")
            base_statement = base_statement.where(search_filter)
            count_base = count_base.where(search_filter)
            
            # Get total count
            total = db.exec(count_base).one()
            
            # Get paginated results
            statement = (
                base_statement
                .order_by(ResourceModel.resource_type)
                .limit(limit)
                .offset(offset)
            )
            resources = db.exec(statement).all()
            
            return PaginatedResources(
                resources=[
                    ResourceSummary(
                        id=resource.id,
                        resource_type=resource.resource_type,
                        documentation_url=resource.documentation_url
                    )
                    for resource in resources
                ],
                total=total,
                limit=limit,
                offset=offset,
                has_more=(offset + limit) < total
            )
        finally:
            db.close()

