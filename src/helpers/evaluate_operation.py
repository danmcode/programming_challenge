from src.helpers.to_dict_syntax import to_dict_syntax


def evaluate_operation(operation, context):
    _context = context
    return eval(to_dict_syntax(operation), {"_context": _context}, {})