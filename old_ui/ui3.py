import tkinter as tk
from tkinter import scrolledtext, messagebox
from tkinter import ttk
from anonymize import anonymize_function, anonymize_prompt, merge_code_and_prompt, rebuild, send_prompt
import threading

class CodeAnonymizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Code Anonymizer - Dark Mode")

        # Dark mode colors
        self.bg_color = "#2e2e2e"
        self.fg_color = "#ffffff"
        self.entry_bg = "#3b3b3b"
        self.entry_fg = "#ffffff"

        root.configure(bg=self.bg_color)

        # Configure grid to expand
        root.grid_rowconfigure(1, weight=1)
        root.grid_rowconfigure(3, weight=1)
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)

        # Code Input
        self.code_label = tk.Label(root, text="Code:", bg=self.bg_color, fg=self.fg_color)
        self.code_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        self.code_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, bg=self.entry_bg, fg=self.entry_fg, insertbackground=self.fg_color)
        self.code_text.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        # Prompt Input
        self.prompt_label = tk.Label(root, text="Prompt:", bg=self.bg_color, fg=self.fg_color)
        self.prompt_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)

        self.prompt_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, bg=self.entry_bg, fg=self.entry_fg, insertbackground=self.fg_color)
        self.prompt_text.grid(row=3, column=0, padx=10, pady=5, sticky="nsew")

        # Buttons
        self.anonymize_button = tk.Button(root, text="Anonymize and Send", command=self.start_anonymize_and_send, bg=self.entry_bg, fg=self.fg_color)
        self.anonymize_button.grid(row=4, column=0, pady=10, padx=10, sticky="e")

        # Tabs for Anonymized and Response
        self.notebook = ttk.Notebook(root)
        self.notebook.grid(row=1, column=1, rowspan=4, padx=10, pady=5, sticky="nsew")

        # Anonymized Output Tab
        self.anonymized_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.anonymized_frame, text="Anonymized")

        self.anonymized_text = scrolledtext.ScrolledText(self.anonymized_frame, wrap=tk.WORD, bg=self.entry_bg, fg=self.entry_fg, insertbackground=self.fg_color)
        self.anonymized_text.pack(expand=True, fill='both', padx=10, pady=5)

        # Response Output Tab
        self.response_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.response_frame, text="Response")

        self.response_text = scrolledtext.ScrolledText(self.response_frame, wrap=tk.WORD, bg=self.entry_bg, fg=self.entry_fg, insertbackground=self.fg_color)
        self.response_text.pack(expand=True, fill='both', padx=10, pady=5)

        # Rebuild Output Tab
        self.rebuild_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.rebuild_frame, text="Rebuilt Response")

        self.rebuild_text = scrolledtext.ScrolledText(self.rebuild_frame, wrap=tk.WORD, bg=self.entry_bg, fg=self.entry_fg, insertbackground=self.fg_color)
        self.rebuild_text.pack(expand=True, fill='both', padx=10, pady=5)

        # Select the "Rebuilt Response" tab as default
        self.notebook.select(self.rebuild_frame)

        # Processing Status
        self.status_label = tk.Label(root, text="", bg=self.bg_color, fg=self.fg_color)
        self.status_label.grid(row=5, column=0, columnspan=2, pady=5)

        # Progress Bar (indeterminate mode)
        self.progress = ttk.Progressbar(root, mode='indeterminate', length=200)
        self.progress.grid(row=6, column=0, columnspan=2, pady=10)

    def start_anonymize_and_send(self):
        # Run the processing in a separate thread to avoid blocking the UI
        threading.Thread(target=self.anonymize_and_send).start()

    def anonymize_and_send(self):
        # Update UI to show processing
        self.status_label.config(text="Processing...")
        self.root.config(cursor="wait")
        self.progress.start()  # Start the progress bar

        # Get user input
        code = self.code_text.get("1.0", tk.END).strip()
        prompt = self.prompt_text.get("1.0", tk.END).strip()

        if not code and not prompt:
            messagebox.showwarning("Input Error", "Please provide code, a prompt, or both.")
            self.stop_processing()
            return

        name_list = []
        anonymized_code = ""
        anonymized_prompt = ""

        # Anonymize code if present
        if code:
            anonymized_code, name_list = anonymize_function(code)

        # Anonymize prompt if present
        if prompt:
            anonymized_prompt = anonymize_prompt(prompt, name_list)

        # Merge code and prompt if both are present
        merged_code_and_prompt = merge_code_and_prompt(anonymized_code, anonymized_prompt)

        # Display anonymized content
        self.anonymized_text.delete("1.0", tk.END)
        self.anonymized_text.insert(tk.END, merged_code_and_prompt)

        # Send to API and get response
        try:
            response = send_prompt(merged_code_and_prompt)
            response_text = response.content[0].text
        except Exception as e:
            messagebox.showerror("API Error", f"Failed to get response: {e}")
            self.stop_processing()
            return

        # Display API response
        self.response_text.delete("1.0", tk.END)
        self.response_text.insert(tk.END, response_text)

        # Rebuild response
        rebuilt_response = rebuild(response_text, name_list)
        self.rebuild_text.delete("1.0", tk.END)
        self.rebuild_text.insert(tk.END, rebuilt_response)

        # Reset UI status
        self.stop_processing()

    def stop_processing(self):
        self.status_label.config(text="")
        self.root.config(cursor="")
        self.progress.stop()  # Stop the progress bar

def main():
    root = tk.Tk()
    app = CodeAnonymizerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
