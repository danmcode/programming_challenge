import logging
import sys
from typing import Dict, Any, List
from src.services.challenge_service import ChallengeService
from src.services.model_service import ModelService
from src.services.pokemon_service import PokemonService
from src.services.swapi_service import SwapiService
from src.models.schemas import Interpretation, Pokemon, Entity, StarWarsPlanet, StarWarsCharacter
import json
import re

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class Application:
    def __init__(self):
        self.challenge_service = ChallengeService()
        self.model_service = ModelService()
        self.pokemon_service = PokemonService()
        self.swapi_service = SwapiService()  # Inicializar el servicio de SWAPI si es necesario
    
    def get_challenge(self) -> Dict[str, Any]:
        try:
            print("Obteniendo el texto del reto...")
            instructions = "Devuélveme la interpretación en formato JSON. Quiero que indiques qué entidades buscar, en qué API, entre la API de pokemon(https://pokeapi.co/) y la API de StarWars (https://swapi.dev/) y qué operaciones realizar. El formato debe ser así:\n{\n  'entities': [\n    {'name': 'Leia Organa', 'attribute': 'height', 'source': 'swapi'},\n    {'name': 'Bulbasaur', 'attribute': 'height', 'source': 'pokeapi'},\n    {'name': 'Owen Lars', 'attribute': 'height', 'source': 'swapi'},\n    {'name': 'Socorro', 'attribute': 'diameter', 'source': 'swapi'}\n  ],\n  'operation': '(Leia.height * Bulbasaur.height * Owen.height) + Socorro.diameter'\n}\nResponde solo con el JSON."
            challenge_text = """En el remoto planeta de Saleucami, conocido por sus vastos desiertos y su población única, un Accelgor, el ágil Pokémon de tipo bicho, decide embarcarse en una aventura matemática. Intrigado por la magnitud de la población del planeta, Accelgor se pregunta qué resultado obtendría al multiplicar su propio peso por la cantidad de habitantes de Saleucami. ¿Qué revelará este cálculo intergaláctico sobre la relación entre el peso de un Pokémon y la vida en un planeta lejano?"""
            
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
            
            response = self.model_service.get_challenge_interpretation(data)
            message_content = response['choices'][0]['message']['content']
            parsed_message = json.loads(message_content.replace("'", '"'))
            
            print("Interpretación del modelo:")
            interpretation = Interpretation(**parsed_message)
            print(interpretation)
            
            "Obtener el pokemón"
            pokemon : Pokemon = {};
            star_wars_model: StarWarsPlanet | StarWarsCharacter = {};
            
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
            
            # Aquí puedes realizar operaciones con los datos obtenidos
            safe_operation = to_dict_syntax(interpretation.operation)
            
            print("👉 Evaluando operación:", safe_operation)
            result = eval(safe_operation, {}, eval_context)
            print(f"\n✅ Resultado final: {result}")
            
            return parsed_message
            
        except Exception as e:
            logger.error(f"Error al procesar la solicitud: {e}")
            raise

def to_dict_syntax(op_str):
    return re.sub(r"(\w+)\.(\w+)", r"\1['\2']", op_str)

def swapi_entity_type(entity: Entity) -> str:
    """Determina el tipo de entidad para la API de Star Wars."""
    planet_attributes = {"population", "diameter", "surface_water", "rotation_period", "orbital_period"}
    character_attributes = {"height", "mass", "homeworld"}
    
    if entity.attribute in planet_attributes:
        return "planets"
    elif entity.attribute in character_attributes:
        return "people"
    else:
        raise ValueError(f"No se pudo determinar el tipo de entidad SWAPI para el atributo '{entity.attribute}'")
    
def main():
    """Función principal de entrada."""
    try:
        app = Application()
        result = app.get_challenge()
        print(json.dumps(result, indent=4, ensure_ascii=False))

    except Exception as e:
        logger.error(f"Error en la aplicación: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()