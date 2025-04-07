import logging
import sys
from typing import Dict, Any, List
from src.services.challenge_service import ChallengeService
from src.services.model_service import ModelService
from src.services.pokemon_service import PokemonService
from src.models.schemas import Interpretation, Pokemon, Entity
import json

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
    
    def get_challenge(self) -> Dict[str, Any]:
        try:
            print("Obteniendo el texto del reto...")
            instructions = "Devuélveme la interpretación en formato JSON. Quiero que indiques qué entidades buscar, en qué API y qué operaciones realizar. El formato debe ser así:\n{\n  'entities': [\n    {'name': 'Leia Organa', 'attribute': 'height', 'source': 'swapi'},\n    {'name': 'Bulbasaur', 'attribute': 'height', 'source': 'pokeapi'},\n    {'name': 'Owen Lars', 'attribute': 'height', 'source': 'swapi'},\n    {'name': 'Socorro', 'attribute': 'diameter', 'source': 'swapi'}\n  ],\n  'operation': '(Leia.height * Bulbasaur.height * Owen.height) + Socorro.diameter'\n}\nResponde solo con el JSON."
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
            
            for entity in interpretation.entities:
                print(f"Nombre: {entity.name}")
                print(f"Atributo: {entity.attribute}")
                print(f"Fuente (API): {entity.source}")
                
                if entity.source == "pokeapi":
                    print("👉 Consultar la PokéAPI")
                    pokemon = self.pokemon_service.get_pokemon(entity.name)
                    print(pokemon)
                elif entity.source == "swapi":
                    print("👉 Consultar la SWAPI")
                else:
                    print("👉 Consultar la SWAPI")
            
            
            return parsed_message
            
        except Exception as e:
            logger.error(f"Error al procesar la solicitud: {e}")
            raise

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