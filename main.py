import tkinter as tk
from tkinter import scrolledtext
from anonymize import anonymize_function, anonymize_prompt, rebuild

def anonymize():
    code = code_text.get("1.0", tk.END).strip()
    prompt = prompt_text.get("1.0", tk.END).strip()
    anonymized_code, name_list = anonymize_function(code)
    anonymized_prompt = anonymize_prompt(prompt, name_list)
    
    anonymized_code_text.delete("1.0", tk.END)
    anonymized_code_text.insert(tk.END, anonymized_code)
    
    name_list_text.delete("1.0", tk.END)
    name_list_text.insert(tk.END, str(name_list))
    
    anonymized_prompt_text.delete("1.0", tk.END)
    anonymized_prompt_text.insert(tk.END, anonymized_prompt)

def rebuild_prompt():
    anonymized_prompt = anonymized_prompt_text.get("1.0", tk.END).strip()
    name_list_str = name_list_text.get("1.0", tk.END).strip()
    name_list = eval(name_list_str)
    
    rebuilt_prompt = rebuild(anonymized_prompt, name_list)
    
    rebuilt_prompt_text.delete("1.0", tk.END)
    rebuilt_prompt_text.insert(tk.END, rebuilt_prompt)

# Create the main window
root = tk.Tk()
root.title("Anonymize and Rebuild Prompt")

# Configure grid to expand with window resize
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_rowconfigure(4, weight=1)
root.grid_rowconfigure(5, weight=1)
root.grid_columnconfigure(1, weight=1)

# Create text areas
tk.Label(root, text="Code:").grid(row=0, column=0, sticky="nsew")
code_text = scrolledtext.ScrolledText(root, width=40, height=10)
code_text.grid(row=0, column=1, sticky="nsew")

tk.Label(root, text="Prompt:").grid(row=1, column=0, sticky="nsew")
prompt_text = scrolledtext.ScrolledText(root, width=40, height=5)
prompt_text.grid(row=1, column=1, sticky="nsew")

tk.Label(root, text="Anonymized Code:").grid(row=2, column=0, sticky="nsew")
anonymized_code_text = scrolledtext.ScrolledText(root, width=40, height=10)
anonymized_code_text.grid(row=2, column=1, sticky="nsew")

tk.Label(root, text="Name Map:").grid(row=3, column=0, sticky="nsew")
name_list_text = scrolledtext.ScrolledText(root, width=40, height=5)
name_list_text.grid(row=3, column=1, sticky="nsew")

tk.Label(root, text="Anonymized Prompt:").grid(row=4, column=0, sticky="nsew")
anonymized_prompt_text = scrolledtext.ScrolledText(root, width=40, height=5)
anonymized_prompt_text.grid(row=4, column=1, sticky="nsew")

tk.Label(root, text="Rebuilt Prompt:").grid(row=5, column=0, sticky="nsew")
rebuilt_prompt_text = scrolledtext.ScrolledText(root, width=40, height=5)
rebuilt_prompt_text.grid(row=5, column=1, sticky="nsew")

# Create buttons
anonymize_button = tk.Button(root, text="Anonymize", command=anonymize)
anonymize_button.grid(row=6, column=0, sticky="nsew")

rebuild_button = tk.Button(root, text="Rebuild", command=rebuild_prompt)
rebuild_button.grid(row=6, column=1, sticky="nsew")

# Start the Tkinter event loop
root.mainloop()
