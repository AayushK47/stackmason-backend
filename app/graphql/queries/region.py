"""Region-related GraphQL queries."""
from typing import List
import strawberry
from sqlmodel import Session, select
from app.database import get_db
from app.models import Region as RegionModel
from app.graphql.types import Region


@strawberry.type
class RegionQueries:
    """Region query resolvers."""
    
    @strawberry.field
    def regions(self, info) -> List[Region]:
        """Get all available AWS regions."""
        db: Session = next(get_db())
        try:
            statement = select(RegionModel).order_by(RegionModel.region_code)
            regions = db.exec(statement).all()
            return [
                Region(
                    id=region.id,
                    region_code=region.region_code,
                    region_name=region.region_name
                )
                for region in regions
            ]
        finally:
            db.close()

