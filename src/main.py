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
        start_time = time.time()
        time_limit = 180
        
        try:
            logger.info("Iniciando prueba oficial...")
            challenge = self.challenge_service.get_challenge()

            while challenge and time.time() - start_time < time_limit:
                try:
                    logger.info(f"Procesando problema ID: {challenge.id}")
                    logger.info(f"Descripción: {challenge.problem}")
                    
                    try:
                        # Resolver el desafío actual
                        result = resolve_challenge(challenge)
                        logger.info(f"Resultado calculado: {result}")

                        # Enviar resultado y obtener el siguiente desafío
                        logger.info("Enviando respuesta...")
                        challenge = self.challenge_service.send_result(result, challenge.id)
                    except Exception as e:
                        logger.error(f"❌ Error al resolver el desafío: {e}")
                        # Obtener un nuevo desafío en caso de error
                        challenge = self.challenge_service.get_challenge()
                        continue
                    
                    if challenge:
                        logger.info(f"Nuevo problema recibido con ID: {challenge.id}")
                    else:
                        logger.info("No quedan más desafíos o se agotó el tiempo.")
                        break
                
                except Exception as e:
                    logger.error(f"❌ Error general en el bucle de prueba: {e}")
                    # Intentar obtener un nuevo desafío
                    challenge = self.challenge_service.get_challenge()

        except Exception as e:
            logger.error(f"❌ Error durante la prueba oficial: {e}", exc_info=True)
            
    
def main():
    """Función principal de entrada."""
    try:
        Application().run_offcial_test()
    except Exception as e:
        logger.error(f"Error en la aplicación: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()