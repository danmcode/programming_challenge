from src.models.schemas import  Entity

def swapi_entity_type(entity: Entity) -> str:
    """Determina el tipo de entidad para la API de Star Wars."""
    planet_attributes = {"population", "diameter", "surface_water", "rotation_period", "orbital_period"}
    character_attributes = {"height", "mass", "homeworld"}
    
    if entity.attribute in planet_attributes:
        return "planets"
    elif entity.attribute in character_attributes:
        return "people"
    else:
        raise ValueError(f"No se pudo determinar el tipo de entidad SWAPI para el atributo '{entity.attribute}'")
