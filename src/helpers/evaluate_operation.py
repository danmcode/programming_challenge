from src.helpers.to_dict_syntax import to_dict_syntax

def evaluate_operation(operation, context, entity_names):
    # Preparar el contexto para evaluación segura
    _context = context
    
    # Convertir la operación a sintaxis de diccionario
    safe_operation = to_dict_syntax(operation, entity_names)
    print(f"👉 Evaluando operación: {safe_operation}")
    
    # Evaluar la expresión con el contexto seguro
    try:
        return eval(safe_operation, {"_context": _context}, {})
    except KeyError as e:
        print(f"Error: No se encontró la clave {e} en el contexto")
        print(f"Contexto disponible: {_context}")
        raise