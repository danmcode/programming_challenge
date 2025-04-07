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

    def get_challenge_interpretation(self, params: Optional[Dict[str, Any]] = None):
        "Obtiene la interpretación del modelo"
        reponse = self.client.post(settings.AI_ENDPOINT, params)
        return reponse