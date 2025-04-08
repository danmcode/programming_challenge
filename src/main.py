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
            #TODO: Cambiar por el endpoint de la API
            challenge_text = """En el bullicioso planeta-ciudad de Coruscant, donde las naves surcan los cielos entre rascacielos infinitos, un Wurmple curioso decide embarcarse en una aventura matemática. Primero, suma su propio peso al periodo orbital del planeta Coruscant, intrigado por la relación entre su diminuto ser y el vasto universo. Sin embargo, la aventura no termina ahí. Kit Fisto, el valiente Maestro Jedi, se une al desafío multiplicando su masa con el peso de un Magikarp. Finalmente, Wurmple resta este producto del resultado anterior. ¿Qué revelará este cálculo intergaláctico en la unión de dos mundos tan diferentes?"""
            logger.info(f"Texto del reto: {challenge_text}\n")
            
            response = self.model_service.get_challenge_interpretation(challenge_text)
            message_content = response['choices'][0]['message']['content']
            parsed_message = json.loads(message_content.replace("'", '"'))
            
            interpretation = Interpretation(**parsed_message)
            logger.info("Interpretación del modelo:")
            logger.info(f"{interpretation}\n")
            
            pokemon : Pokemon = {};
            eval_context = {}
            
            for entity in interpretation.entities:
                if entity.source == "pokeapi":
                    pokemon = self.pokemon_service.get_pokemon(entity.name)
                    value = getattr(pokemon, entity.attribute)
                    eval_context.setdefault(entity.name, {})[entity.attribute] = value

                elif entity.source == "swapi":
                    entity_type = swapi_entity_type(entity)
                    sw_model = self.swapi_service.get_swapi_data(entity_type, entity)
                    value_str = getattr(sw_model, entity.attribute)
                    
                    if value_str == "unknown":
                        raise ValueError(f"Atributo desconocido: {entity.attribute}")
                    
                    value = float(value_str.replace(",", ""))
                    eval_context.setdefault(entity.name, {})[entity.attribute] = value
            
            safe_operation = to_dict_syntax(interpretation.operation)
            
            #TODO: PONERLO EN UN LOG DE TEXTO
            logger.info("👉 Evaluando operación:", safe_operation)
            result = evaluate_operation(interpretation.operation, eval_context)
            logger.info(f"Resultado de la operación: {result}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error al procesar la solicitud: {e}")
            raise

def main():
    """Función principal de entrada."""
    try:
        app = Application()
        result = app.get_challenge()
        print(f"Resultado: {result}")

    except Exception as e:
        logger.error(f"Error en la aplicación: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()