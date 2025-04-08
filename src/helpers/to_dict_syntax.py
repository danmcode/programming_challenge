import re

def to_dict_syntax(op_str, entity_names=None):
    """
    Convierte expresiones con notación de punto a sintaxis de diccionario.
    
    Args:
        op_str: String con la operación a convertir
        entity_names: Lista de nombres completos de entidades para mapeo correcto
    
    Returns:
        String con la operación convertida a sintaxis de diccionario
    """
    if entity_names is None:
        entity_names = []
    
    # Crea un mapa de nombres parciales a nombres completos
    name_map = {}
    for full_name in entity_names:
        # Agrega el nombre completo
        name_map[full_name] = full_name
        
        # Agrega el primer nombre (para casos como "Boba Fett" -> "Boba")
        if " " in full_name:
            first_name = full_name.split(" ")[0]
            name_map[first_name] = full_name
        
        # Agrega el primer nombre antes del guión (para casos como "Ki-Adi-Mundi" -> "Ki")
        if "-" in full_name:
            first_part = full_name.split("-")[0]
            name_map[first_part] = full_name
    
    # Patrón para detectar referencias a atributos: nombre.atributo
    pattern = r'([A-Za-z0-9\-_ ]+)\.([A-Za-z0-9_]+)'
    
    def replacement(match):
        entity_name = match.group(1).strip()
        attribute = match.group(2)
        
        # Usar el nombre completo si está en el mapa
        full_name = name_map.get(entity_name, entity_name)
        
        return f"_context['{full_name}']['{attribute}']"
    
    return re.sub(pattern, replacement, op_str)