from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class StarWarsPlanet(BaseModel):
    """Modelo para datos de planetas de Star Wars."""
    name: str
    rotation_period: int
    orbital_period: int
    diameter: int
    surface_water: int
    population: int

class StarWarsCharacter(BaseModel):
    name: str
    height: int
    mass: int
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