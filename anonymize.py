import ast
import astor
import re
import builtins
from anthropic_api_call import send_prompt

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
    if node.id in dir(builtins):
        return node  
    if node.id not in name_map:
        new_name = f"var{counter[0]}"
        save_name(node.id, new_name, name_map, name_list)
        counter[0] += 1
    node.id = name_map[node.id]
    return node


def anonymize_attribute(node, name_map, name_list, counter):
    return node  


# def anonymize_attribute(node, name_map, name_list, counter):
#     if node.attr not in name_map:
#         new_name = f"attr{counter[0]}"
#         save_name(node.attr, new_name, name_map, name_list)
#         counter[0] += 1
#     node.attr = name_map[node.attr]
#     return node

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

def merge_code_and_prompt(code, prompt):
    return f"{code}\n\n{prompt}"

# def test_1():
#     code = """
# import datetime

# def get_current_time():
#     current_time = datetime.datetime.now().strftime("%I:%M %p")
#     return f"The current time is {current_time}"

# # Example usage
# print(get_current_time())
#     """

#     anonymized_code, name_list1 = anonymize_function(code)

#     print("Anonymized code:")
#     print(anonymized_code)
    


# Example usage
def main():
    code = """
import datetime

def get_current_time():
    current_time = datetime.datetime.now().time()
    return current_time.strftime("%H:%M:%S")

# Example usage
print(get_current_time())
    """

    prompt = "Can you explain how the function save_name works?"

    anonymized_code, name_list1 = anonymize_function(code)
    anonymized_prompt = anonymize_prompt(prompt, name_list1)
    anonymize_merged_code_and_prompt = merge_code_and_prompt(anonymized_code, anonymized_prompt)


    print("Anonymized code and Prompt:")
    print(anonymize_merged_code_and_prompt)
    print("\n")

    response = send_prompt(anonymize_merged_code_and_prompt)

    # Extracting the text content from the response object
    response_text = response.content[0].text
    print("Response:")
    print(response_text)

    rebuilt_response = rebuild(response_text, name_list1)
    print("Rebuilt response:")
    print(rebuilt_response)

if __name__ == "__main__":
    main()
