from typing import Dict, List, Any, Optional

from src.api.client import APIClient
from src.config.settings import settings
from src.models.schemas import Entity, StarWarsCharacter, StarWarsPlanet


class SwapiService:
    
    def __init__(self):
        self.client = APIClient(
            base_url=settings.SWAPI,
            api_key=settings.API_KEY,
            timeout=settings.API_TIMEOUT
        )

    def get_swapi_data(self, type: str, entity: Entity):
        "Obtiene la data de la API de Star Wars, buscando por el tipo y la entidad"
        url = f"{type}/?search={entity.name}"
        
        response = self.client.get(url)
        
        first_result = response["results"][0]

        if type == "people":
            return StarWarsCharacter(**first_result)
        elif type == "planets":
            return StarWarsPlanet(**first_result)
        else:
            raise ValueError(f"Tipo desconocido de SWAPI: {type}")

