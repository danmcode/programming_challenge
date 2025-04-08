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
        
        reponse = self.client.get(settings.PROD_ENDPOINT)
        logger.info(f"***RESPUESTA DEL ENDPONT DEL RETO***: {reponse}\n\n")
        challenge = Challenge(**reponse)
        return challenge
    
    def send_result(self, result: float, challenge_id):
        "Envía el resultado al endpoint de la API"
        
        data = {
            "problem_id": challenge_id,
            "answer": result
        }
        
        logger.info(f"***DATA ENVIADA***\n: {data}\n\n")
        response = self.client.post(settings.SOLUTION_ENDPOINT, data)
        logger.info(f"***RESPUESTA DEL ENDPONT DEL RESULTADO***\n: {response}\n\n")
        
        if response and 'next_problem' in response:
            next_challenge = Challenge(**response['next_problem'])
            return next_challenge
        else:
            logger.info("No hay más problemas disponibles")
            return None