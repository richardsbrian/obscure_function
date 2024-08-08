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
    anonymized_prompt = new_anonymized_prompt_text.get("1.0", tk.END).strip()
    name_list_str = name_list_text.get("1.0", tk.END).strip()
    name_list = eval(name_list_str)
    
    rebuilt_prompt = rebuild(anonymized_prompt, name_list)
    
    rebuilt_prompt_text.delete("1.0", tk.END)
    rebuilt_prompt_text.insert(tk.END, rebuilt_prompt)

    rebuilt_code, _ = rebuild(new_anonymized_code_text.get("1.0", tk.END).strip(), name_list)
    rebuilt_code_text.delete("1.0", tk.END)
    rebuilt_code_text.insert(tk.END, rebuilt_code)

# Create the main window
root = tk.Tk()
root.title("Anonymize and Rebuild Prompt")

# Configure grid to expand with window resize
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_columnconfigure(1, weight=1)

# Section 1
section1 = tk.LabelFrame(root, text="Section 1")
section1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

section1.grid_rowconfigure(0, weight=1)
section1.grid_rowconfigure(1, weight=1)
section1.grid_rowconfigure(2, weight=1)
section1.grid_rowconfigure(3, weight=1)
section1.grid_rowconfigure(4, weight=1)
section1.grid_columnconfigure(1, weight=1)

tk.Label(section1, text="Code:").grid(row=0, column=0, sticky="nsew")
code_text = scrolledtext.ScrolledText(section1, width=40, height=10)
code_text.grid(row=0, column=1, sticky="nsew")

tk.Label(section1, text="Prompt:").grid(row=1, column=0, sticky="nsew")
prompt_text = scrolledtext.ScrolledText(section1, width=40, height=5)
prompt_text.grid(row=1, column=1, sticky="nsew")

tk.Label(section1, text="Anonymized Code:").grid(row=2, column=0, sticky="nsew")
anonymized_code_text = scrolledtext.ScrolledText(section1, width=40, height=10)
anonymized_code_text.grid(row=2, column=1, sticky="nsew")

tk.Label(section1, text="Anonymized Prompt:").grid(row=3, column=0, sticky="nsew")
anonymized_prompt_text = scrolledtext.ScrolledText(section1, width=40, height=5)
anonymized_prompt_text.grid(row=3, column=1, sticky="nsew")

anonymize_button = tk.Button(section1, text="Anonymize", command=anonymize)
anonymize_button.grid(row=4, column=0, columnspan=2, sticky="nsew")

# Section 2
section2 = tk.LabelFrame(root, text="Section 2")
section2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

section2.grid_rowconfigure(0, weight=1)
section2.grid_rowconfigure(1, weight=1)
section2.grid_rowconfigure(2, weight=1)
section2.grid_rowconfigure(3, weight=1)
section2.grid_rowconfigure(4, weight=1)
section2.grid_columnconfigure(1, weight=1)

tk.Label(section2, text="New Anonymized Code:").grid(row=0, column=0, sticky="nsew")
new_anonymized_code_text = scrolledtext.ScrolledText(section2, width=40, height=10)
new_anonymized_code_text.grid(row=0, column=1, sticky="nsew")

tk.Label(section2, text="New Anonymized Prompt:").grid(row=1, column=0, sticky="nsew")
new_anonymized_prompt_text = scrolledtext.ScrolledText(section2, width=40, height=5)
new_anonymized_prompt_text.grid(row=1, column=1, sticky="nsew")

tk.Label(section2, text="Rebuilt Code:").grid(row=2, column=0, sticky="nsew")
rebuilt_code_text = scrolledtext.ScrolledText(section2, width=40, height=10)
rebuilt_code_text.grid(row=2, column=1, sticky="nsew")

tk.Label(section2, text="Rebuilt Prompt:").grid(row=3, column=0, sticky="nsew")
rebuilt_prompt_text = scrolledtext.ScrolledText(section2, width=40, height=5)
rebuilt_prompt_text.grid(row=3, column=1, sticky="nsew")

rebuild_button = tk.Button(section2, text="Rebuild", command=rebuild_prompt)
rebuild_button.grid(row=4, column=0, columnspan=2, sticky="nsew")

# Hide the name map text area
name_list_text = tk.Text(root, height=1, width=1)
name_list_text.grid(row=2, column=2)

# Start the Tkinter event loop
root.mainloop()
