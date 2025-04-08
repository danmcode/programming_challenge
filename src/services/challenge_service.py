from typing import Dict, List, Any, Optional
from datetime import datetime

from src.api.client import APIClient
from src.config.settings import settings
from src.models.schemas import Challenge
from src.config.logger import get_logger

logger = get_logger(__name__)

class ChallengeService:
    
    def __init__(self):
        self.client = APIClient(
            base_url=settings.API_BASE_URL,
            api_key=settings.API_KEY,
            timeout=settings.API_TIMEOUT
        )

    def get_challenge(self):
        "Obtiene el desafío desde el enpoint de la API"
        
        reponse = self.client.get(settings.TEST_ENDPOINT)
        logger.info(f"***RESPUESTA DEL ENDPONT DEL RETO***: {reponse}\n\n")
        challenge = Challenge(**reponse)
        return challenge