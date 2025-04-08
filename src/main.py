import logging
import sys
from typing import Dict, Any, List
from src.helpers.evaluate_operation import evaluate_operation
from src.helpers.swapi_entity_type import swapi_entity_type
from src.helpers.to_dict_syntax import to_dict_syntax
from src.services.challenge_service import ChallengeService
from src.services.model_service import ModelService
from src.services.pokemon_service import PokemonService
from src.services.swapi_service import SwapiService
from src.models.schemas import Interpretation, Pokemon
from src.config.logger import get_logger
import json

logger = get_logger(__name__)

class Application:
    def __init__(self):
        self.challenge_service = ChallengeService()
        self.model_service = ModelService()
        self.pokemon_service = PokemonService()
        self.swapi_service = SwapiService()
    
    def get_challenge(self) -> Dict[str, Any]:
        try:
            logger.info("Obteniendo el texto del reto...\n")
            challenge_text = self.challenge_service.get_challenge().problem
            logger.info(f"Texto del reto: {challenge_text}\n")
            
            response = self.model_service.get_challenge_interpretation(challenge_text)
            message_content = response['choices'][0]['message']['content']
            parsed_message = json.loads(message_content.replace("'", '"'))
            
            interpretation = Interpretation(**parsed_message)
            logger.info("Interpretación del modelo:")
            logger.info(f"{interpretation}\n")
            
            pokemon : Pokemon = {};
            eval_context = {}
            entity_names = [entity.name for entity in interpretation.entities]
            
            for entity in interpretation.entities:
                if entity.source == "pokeapi":
                    pokemon = self.pokemon_service.get_pokemon(entity.name)
                    value = getattr(pokemon, entity.attribute)
                    eval_context[entity.name] = {entity.attribute: value}

                elif entity.source == "swapi":
                    entity_type = swapi_entity_type(entity)
                    sw_model = self.swapi_service.get_swapi_data(entity_type, entity)
                    value_str = getattr(sw_model, entity.attribute)
                    
                    if value_str == "unknown":
                        raise ValueError(f"Atributo desconocido: {entity.attribute}")
                    
                    value = float(value_str.replace(",", ""))
                    eval_context[entity.name] = {entity.attribute: value}
            
            safe_operation = to_dict_syntax(interpretation.operation, entity_names)
            
            logger.info("Evaluando operación: %s", safe_operation)
            result = eval(safe_operation, {"_context": eval_context}, {})
            rounded_result = round(result, 10)
            logger.info(f"Resultado de la operación: {rounded_result}")
            
            return rounded_result
            
        except Exception as e:
            logger.error(f"Error al procesar la solicitud: {e}")
            raise

def main():
    """Función principal de entrada."""
    try:
        Application().get_challenge()
    except Exception as e:
        logger.error(f"Error en la aplicación: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()