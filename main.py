import ast
import astor

def anonymize_function(code):
    """
    Anonymizes function names, argument names, variable names, class names,
    method names, and attributes in the provided code.
    
    Args:
    - code (str): The source code to anonymize.
    
    Returns:
    - str: The anonymized source code.
    """
    tree = ast.parse(code)
    
    def anonymize_node(node, name_map, counter):
        if isinstance(node, ast.FunctionDef):
            node.name = "function"
            local_name_map = {}
            local_counter = 0
            
            def anonymize_arg(arg):
                nonlocal local_counter
                if arg.arg not in local_name_map:
                    local_name_map[arg.arg] = f"var{local_counter}"
                    local_counter += 1
                arg.arg = local_name_map[arg.arg]
                return arg
            
            def anonymize_name(name):
                if name.id not in local_name_map:
                    local_name_map[name.id] = f"var{local_counter}"
                    local_counter += 1
                name.id = local_name_map[name.id]
                return name
            
            node.args.args = [anonymize_arg(arg) for arg in node.args.args]
            combined_name_map = {**name_map, **local_name_map}
            
            for i, n in enumerate(node.body):
                node.body[i] = anonymize_node(n, combined_name_map, counter)
            return node
        
        elif isinstance(node, ast.ClassDef):
            if node.name not in name_map:
                name_map[node.name] = f"class{counter[0]}"
                counter[0] += 1
            node.name = name_map[node.name]
            method_counter = 0
            for i, n in enumerate(node.body):
                if isinstance(n, ast.FunctionDef):
                    if n.name not in name_map:
                        name_map[n.name] = f"method{method_counter}"
                        method_counter += 1
                    n.name = name_map[n.name]
                node.body[i] = anonymize_node(n, name_map, counter)
            return node
        
        elif isinstance(node, ast.Name):
            if node.id not in name_map:
                name_map[node.id] = f"var{counter[0]}"
                counter[0] += 1
            node.id = name_map[node.id]
            return node
        
        elif isinstance(node, ast.Attribute):
            if node.attr not in name_map:
                name_map[node.attr] = f"attr{counter[0]}"
                counter[0] += 1
            node.attr = name_map[node.attr]
            return node
        
        for field, value in ast.iter_fields(node):
            if isinstance(value, list):
                value[:] = [anonymize_node(item, name_map, counter) if isinstance(item, ast.AST) else item for item in value]
            elif isinstance(value, ast.AST):
                setattr(node, field, anonymize_node(value, name_map, counter))
        
        return node
    
    anonymized_tree = anonymize_node(tree, {}, [0])
    return astor.to_source(anonymized_tree)

# Example usage
code1 = """
def add_100(balance):
    balance += 100
    return balance
"""

code2 = """
def multiply(x, y):
    result = x * y
    return result
"""

code3 = """
def complex_function(a, b, c):
    temp = a + b
    temp2 = temp * c
    if temp2 > 10:
        return temp2
    else:
        return 0
"""

code4 = """
class Example:
    def __init__(self, value):
        self.value = value
    
    def get_value(self):
        return self.value
"""

anonymized_code1 = anonymize_function(code1)
anonymized_code2 = anonymize_function(code2)
anonymized_code3 = anonymize_function(code3)
anonymized_code4 = anonymize_function(code4)

print("Anonymized Code 1:")
print(anonymized_code1)
print("Anonymized Code 2:")
print(anonymized_code2)
print("Anonymized Code 3:")
print(anonymized_code3)
print("Anonymized Code 4:")
print(anonymized_code4)
