import sys
from src.services.challenge_service import ChallengeService
from src.config.logger import get_logger
from src.helpers.resolve_challenge import resolve_challenge
import time

logger = get_logger(__name__)

class Application:
    
    def __init__(self):
        self.challenge_service = ChallengeService()

    def run_offcial_test(self):
        """Versión del test oficial"""
        start_time = time.time()
        time_limit = 180
        
        try:
            logger.info("⏱️ Iniciando prueba oficial...")
            challenge = self.challenge_service.get_challenge()

            while time.time() - start_time < time_limit:
                try:
                    logger.info("🧩 Nuevo problema recibido")
                    last_result = resolve_challenge(challenge)

                    logger.info("📤 Enviando respuesta...")
                    challenge = self.challenge_service.send_result(last_result, challenge.id)

                    if not challenge:
                        logger.info("✅ No quedan más desafíos o se agotó el tiempo.")
                        break
                
                except Exception as e:
                    logger.error(f"❌ Error al resolver el desafío: {e}")
                    continue

        except Exception as e:
            logger.error(f"❌ Error durante la prueba oficial: {e}")
            
    
def main():
    """Función principal de entrada."""
    try:
        Application().run_offcial_test()
    except Exception as e:
        logger.error(f"Error en la aplicación: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()