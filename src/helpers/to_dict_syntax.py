import re

def to_dict_syntax(op_str):
    pattern = r'([A-Za-z0-9\- ]+)\.([A-Za-z0-9_]+)'
    
    def replacement(match):
        entity_name = match.group(1).strip()
        attribute = match.group(2)
        
        safe_name = entity_name.replace('-', '_minus_').replace(' ', '_space_')
        
        return f"_context['{entity_name}']['{attribute}']"
    
    return re.sub(pattern, replacement, op_str)