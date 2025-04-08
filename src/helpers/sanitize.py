import re
import keyword
from typing import Dict
from src.models.schemas import Interpretation

def sanitize_key(key: str) -> str:
    """Sanitiza un nombre compuesto name.attribute para que sea una variable Python válida."""
    sanitized = re.sub(r'[^a-zA-Z0-9_]', '_', key)  # Reemplaza caracteres no válidos
    if re.match(r'^\d', sanitized):  # Si empieza con número
        sanitized = f"var_{sanitized}"
    if sanitized in keyword.kwlist:  # Si es palabra reservada
        sanitized += "_var"
    return sanitized

def sanitize_operation(operation: str, context_keys: list[str]) -> str:
    """Reemplaza cada name.attribute en la operación por su versión sanitizada."""
    sorted_keys = sorted(context_keys, key=len, reverse=True)
    for original in sorted_keys:
        safe = sanitize_key(original)
        operation = operation.replace(original, safe)
    return operation

def build_safe_context(interpretation: Interpretation, eval_context: Dict[str, Dict[str, float]]) -> Dict[str, float]:
    """Construye un diccionario plano {name_attribute: value} listo para evaluación."""
    flat_context = {}
    for entity in interpretation.entities:
        key = f"{entity.name}.{entity.attribute}"
        safe_key = sanitize_key(key)
        value = eval_context.get(entity.name, {}).get(entity.attribute, 0)
        flat_context[safe_key] = value
    return flat_context

def evaluate_operation(interpretation: Interpretation, eval_context: Dict[str, Dict[str, float]]) -> float:
    """
    Evalúa la operación definida en la interpretación, utilizando el contexto con valores de entidades.
    Retorna el resultado como float (redondeado), o 0 si hay errores.
    """
    try:
        flat_context = build_safe_context(interpretation, eval_context)
        operation_keys = [f"{e.name}.{e.attribute}" for e in interpretation.entities]
        safe_operation = sanitize_operation(interpretation.operation, operation_keys)

        result = eval(safe_operation, {}, flat_context)
        return round(result, 10)
    except Exception as e:
        print(f"[ERROR] Falló la evaluación: {e}")
        return 0
