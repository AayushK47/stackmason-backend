"""GraphQL types for regions."""
import strawberry


@strawberry.type
class Region:
    """AWS Region type."""
    id: int
    region_code: str
    region_name: str

