import ast
import astor
import re

def save_name(name, new_name, name_map, name_list):
    name_map[name] = new_name
    name_list.append({name: new_name})

def anonymize_function(code):
    tree = ast.parse(code)
    name_map = {}
    name_list = []
    anonymized_tree = anonymize_node(tree, name_map, name_list, [0])
    return astor.to_source(anonymized_tree), name_list

def anonymize_node(node, name_map, name_list, counter):
    if isinstance(node, ast.FunctionDef):
        return anonymize_function_def(node, name_map, name_list, counter)
    elif isinstance(node, ast.ClassDef):
        return anonymize_class_def(node, name_map, name_list, counter)
    elif isinstance(node, ast.Name):
        return anonymize_name(node, name_map, name_list, counter)
    elif isinstance(node, ast.Attribute):
        return anonymize_attribute(node, name_map, name_list, counter)
    
    for field, value in ast.iter_fields(node):
        if isinstance(value, list):
            value[:] = [anonymize_node(item, name_map, name_list, counter) if isinstance(item, ast.AST) else item for item in value]
        elif isinstance(value, ast.AST):
            setattr(node, field, anonymize_node(value, name_map, name_list, counter))
    
    return node

def anonymize_function_def(node, name_map, name_list, counter):
    save_name(node.name, f"function{counter[0]}", name_map, name_list)
    node.name = f"function{counter[0]}"
    counter[0] += 1
    
    def anonymize_arg(arg):
        if arg.arg not in name_map:
            new_name = f"var{counter[0]}"
            save_name(arg.arg, new_name, name_map, name_list)
            counter[0] += 1
        arg.arg = name_map[arg.arg]
        return arg
    
    node.args.args = [anonymize_arg(arg) for arg in node.args.args]
    
    for i, n in enumerate(node.body):
        node.body[i] = anonymize_node(n, name_map, name_list, counter)
    return node

def anonymize_class_def(node, name_map, name_list, counter):
    if node.name not in name_map:
        new_name = f"class{counter[0]}"
        save_name(node.name, new_name, name_map, name_list)
        counter[0] += 1
    node.name = name_map[node.name]
    method_counter = 0
    for i, n in enumerate(node.body):
        if isinstance(n, ast.FunctionDef):
            if n.name not in name_map:
                new_name = f"method{method_counter}"
                save_name(n.name, new_name, name_map, name_list)
                method_counter += 1
            n.name = name_map[n.name]
        node.body[i] = anonymize_node(n, name_map, name_list, counter)
    return node

def anonymize_name(node, name_map, name_list, counter):
    if node.id not in name_map:
        new_name = f"var{counter[0]}"
        save_name(node.id, new_name, name_map, name_list)
        counter[0] += 1
    node.id = name_map[node.id]
    return node

def anonymize_attribute(node, name_map, name_list, counter):
    if node.attr not in name_map:
        new_name = f"attr{counter[0]}"
        save_name(node.attr, new_name, name_map, name_list)
        counter[0] += 1
    node.attr = name_map[node.attr]
    return node

def rebuild(anonymized_code, name_list):
    for mapping in reversed(name_list):
        for original_name, anonymized_name in mapping.items():
            anonymized_code = anonymized_code.replace(anonymized_name, original_name)
    return anonymized_code

def anonymize_prompt(prompt, name_list):
    for mapping in name_list:
        for original_name, anonymized_name in mapping.items():
            prompt = re.sub(rf'\b{original_name}\b', anonymized_name, prompt)
    return prompt

# Example usage
code1 = """
def multiply_checks(x, y):
    total = x * y
    return total
"""

prompt = "Can you explain how multiply_checks function works and how variables x and y are used?"

anonymized_code1, name_list1 = anonymize_function(code1)
anonymized_prompt = anonymize_prompt(prompt, name_list1)

print("Original Code 1:")
print(code1)
print("Anonymized Code 1:")
print(anonymized_code1)
print("Name Map 1:")
print(name_list1)
print("\n")
print("Original Prompt:")
print(prompt)
print("\n")
print("Anonymized Prompt:")
print(anonymized_prompt)
print("\n")


rebuilt_prompt = rebuild(anonymized_prompt, name_list1)
print("Rebuilt prompt 1:")
print(rebuilt_prompt)
print("\n")


# Rebuild the original code
rebuilt_code1 = rebuild(anonymized_code1, name_list1)
print("Rebuilt Code 1:")
print(rebuilt_code1)





code2 = """
def multiply_checks(x, y):
    total = x * y
    return total
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

#anonymized_code2, name_map2 = anonymize_function(code2)
#anonymized_code3, name_map3 = anonymize_function(code3)
#anonymized_code4, name_map4 = anonymize_function(code4)



# print("Anonymized Code 2:")
# print(anonymized_code2)
# print("Name Map 2:")
# print(name_map2)

# print("Anonymized Code 3:")
# print(anonymized_code3)
# print("Name Map 3:")
# print(name_map3)

# print("Anonymized Code 4:")
# print(anonymized_code4)
# print("Name Map 4:")
# print(name_map4)
