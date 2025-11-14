"""Utility functions for building property trees."""
from sqlmodel import Session, select
from app.models import Property as PropertyModel, PropertyType as PropertyTypeModel
from app.graphql.types import PropertyDetail


def build_property_tree(property_obj: PropertyModel, db: Session, visited_types: set = None) -> PropertyDetail:
    """Recursively build property tree with nested properties."""
    if visited_types is None:
        visited_types = set()
    
    complex_type_name = None
    nested_properties = None
    
    # If this property has a complex type, get its nested properties
    if property_obj.complex_type_id:
        statement = select(PropertyTypeModel).where(
            PropertyTypeModel.id == property_obj.complex_type_id
        )
        complex_type = db.exec(statement).first()
        
        if complex_type:
            complex_type_name = complex_type.type_name
            
            # Avoid infinite recursion for circular references
            if complex_type.id not in visited_types:
                visited_types.add(complex_type.id)
                
                # Get properties of this complex type
                nested_statement = select(PropertyModel).where(
                    PropertyModel.property_type_id == complex_type.id
                )
                nested_props = db.exec(nested_statement).all()
                
                nested_properties = [
                    build_property_tree(prop, db, visited_types.copy())
                    for prop in nested_props
                ]
    
    return PropertyDetail(
        id=property_obj.id,
        property_name=property_obj.property_name,
        documentation_url=property_obj.documentation_url,
        update_type=property_obj.update_type,
        is_required=property_obj.is_required or False,
        is_list=property_obj.is_list or False,
        is_map=property_obj.is_map or False,
        primitive_type=property_obj.primitive_type,
        complex_type_id=property_obj.complex_type_id,
        complex_type_name=complex_type_name,
        list_allows_duplicates=property_obj.list_allows_duplicates,
        nested_properties=nested_properties
    )

