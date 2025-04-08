from src.helpers.swapi_entity_type import swapi_entity_type
# from src.helpers.to_dict_syntax import to_dict_syntax
from src.helpers.sanitize import evaluate_operation
from src.models.schemas import Interpretation, Challenge
from src.config.logger import get_logger
from src.services.model_service import ModelService
from src.services.pokemon_service import PokemonService
from src.services.swapi_service import SwapiService
import json

logger = get_logger(__name__)

def resolve_challenge(challenge: Challenge):
    model_service = ModelService()
    pokemon_service = PokemonService()
    swapi_service = SwapiService()
    
    try:
        logger.info("Obteniendo el texto del reto...\n")
        logger.info(f"Texto del reto: {challenge.problem}\n")
        
        response = model_service.get_challenge_interpretation(challenge.problem)
        message_content = response['choices'][0]['message']['content']
        
        # Asegurarse de que el mensaje pueda ser parseado como JSON
        try:
            parsed_message = json.loads(message_content.replace("'", '"'))
        except json.JSONDecodeError as e:
            logger.error(f"Error al parsear JSON: {e}")
            logger.error(f"Contenido recibido: {message_content}")
            return 0
        
        try:
            interpretation = Interpretation(**parsed_message)
            logger.info("Interpretación del modelo:")
            logger.info(f"{interpretation}\n")
        except Exception as e:
            logger.error(f"Error al crear objeto Interpretation: {e}")
            return 0
        
        eval_context = {}
        
        # Recolectar valores para la operación
        for entity in interpretation.entities:
            try:
                if entity.source == "pokeapi":
                    pokemon = pokemon_service.get_pokemon(entity.name)
                    value = getattr(pokemon, entity.attribute)
                    eval_context[entity.name] = {entity.attribute: value}

                elif entity.source == "swapi":
                    entity_type = swapi_entity_type(entity)
                    sw_model = swapi_service.get_swapi_data(entity_type, entity)
                    value_str = getattr(sw_model, entity.attribute)
                    
                    if value_str == "unknown":
                        logger.warning(f"Atributo desconocido: {entity.attribute} para {entity.name}")
                        value_str = "0"  # Valor predeterminado para no interrumpir
                    
                    value = float(value_str.replace(",", ""))
                    eval_context[entity.name] = {entity.attribute: value}
            except Exception as e:
                logger.error(f"Error procesando entidad {entity.name}: {e}")
                eval_context[entity.name] = {entity.attribute: 0}  # Valor predeterminado
        
        # Imprimir el contexto para depuración
        logger.debug(f"Contexto de evaluación: {eval_context}")
        
        result = evaluate_operation(interpretation, eval_context)
        logger.info(f"Resultado de la operación: {result}")
        return result
            
    except Exception as e:
        logger.error(f"Error general al procesar la solicitud: {e}")
        return 0