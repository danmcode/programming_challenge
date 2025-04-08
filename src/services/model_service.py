from typing import Dict, List, Any, Optional

from src.api.client import APIClient
from src.config.settings import settings

class ModelService:
    
    def __init__(self):
        self.client = APIClient(
            base_url=settings.API_BASE_URL,
            api_key=settings.API_KEY,
            timeout=settings.API_TIMEOUT
        )

    def get_challenge_interpretation(self, challenge_text: str):
        "Obtiene la interpretación del modelo"
        instructions = "Devuélveme la interpretación en formato JSON. Quiero que indiques qué entidades buscar, en qué API, entre la API de pokemon(https://pokeapi.co/) y la API de StarWars (https://swapi.dev/) y qué operaciones realizar. El formato debe ser así:\n{\n  'entities': [\n    {'name': 'Leia Organa', 'attribute': 'height', 'source': 'swapi'},\n    {'name': 'Bulbasaur', 'attribute': 'height', 'source': 'pokeapi'},\n    {'name': 'Owen Lars', 'attribute': 'height', 'source': 'swapi'},\n    {'name': 'Socorro', 'attribute': 'diameter', 'source': 'swapi'}\n  ],\n  'operation': '(Leia.height * Bulbasaur.height * Owen.height) + Socorro.diameter'\n}\nResponde solo con el JSON. NOTA: Solo cuando diga water_surface sin mas cambiar, por surface_water"
        
        data = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "developer",
                    "content": instructions
                },
                {
                    "role": "user",
                    "content": challenge_text
                }
            ],
        }
        
        reponse = self.client.post(settings.AI_ENDPOINT, data)
        return reponse