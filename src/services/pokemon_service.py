from typing import Dict, List, Any, Optional

from src.api.client import APIClient
from src.config.settings import settings
from src.models.schemas import Pokemon

class PokemonService:
    
    def __init__(self):
        self.client = APIClient(
            base_url=settings.POKE_API,
            api_key=settings.API_KEY,
            timeout=settings.API_TIMEOUT
        )

    def get_pokemon(self, pokemon: str):
        "Obtiene la interpretación del modelo"
        url = f"pokemon/{pokemon.lower()}"
        response = self.client.get(url)
        pokemon_data = Pokemon(**response)
        return pokemon_data