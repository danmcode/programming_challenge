from pydantic import BaseModel
from typing import List

class StarWarsPlanet(BaseModel):
    """Modelo para datos de planetas de Star Wars."""
    name: str
    rotation_period: str
    orbital_period: str
    diameter: str
    surface_water: str
    population: str

class StarWarsCharacter(BaseModel):
    name: str
    height: str
    mass: str
    homeworld: str
    
class Pokemon(BaseModel):
    """Modelo para datos de Pokémon."""
    name: str
    base_experience: int
    height: float
    weight: float

class Challenge(BaseModel):
    """Modelo para el desafío."""
    id: str
    problem: str
    
class Entity(BaseModel):
    """Modelo para entidades del desafío."""
    name: str
    attribute: str
    source: str

class Interpretation(BaseModel):
    """Modelo para la interpretación del desafío."""
    entities: List[Entity]
    operation: str