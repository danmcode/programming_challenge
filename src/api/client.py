import requests
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class APIClient:
    """Cliente base para realizar peticiones HTTP a APIs externas."""
    
    def __init__(self, base_url: str, api_key: str, timeout: int = 30):
        self.base_url = base_url
        self.api_key = api_key
        self.timeout = timeout
        self.session = requests.Session()
        
    def _get_headers(self) -> Dict[str, str]:
        """Retorna los headers comunes para todas las peticiones."""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Realiza una petición GET a la API."""
        url = f"{self.base_url}/{endpoint}"
        try:
            response = self.session.get(
                url,
                headers=self._get_headers(),
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error en petición GET a {url}: {e}")
            raise
    
    def post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Realiza una petición POST a la API."""
        url = f"{self.base_url}/{endpoint}"
        try:
            response = self.session.post(
                url,
                headers=self._get_headers(),
                json=data,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error en petición POST a {url}: {e}")
            raise