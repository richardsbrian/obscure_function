# Python Code & Prompt Anonymizer

![Anonymize_logo](https://github.com/user-attachments/assets/76e22121-45c8-454e-8e8b-02d63f66a5b6)

This is a Flask-based application designed exclusively for anonymizing Python code and associated prompts. The app sends anonymized content to an external API, receives processed responses, and reconstructs the original identifiers from the API output. It includes a responsive web interface for user interaction.

---

## Features

- **Python Code Anonymization**: Strips sensitive identifiers (e.g., function names, variable names) from Python code and replaces them with anonymized placeholders.
- **Prompt Anonymization**: Maps sensitive terms in prompts using the anonymization mappings generated from the code.
- **Submission**: Combines anonymized code and prompts for submission to the external API.
- **Response Reconstruction**: Rebuilds API responses with original identifiers.
- **Web Interface**: Interactive UI to input Python code and prompts, view anonymized results, and rebuilt responses.

---

## Requirements

- Python 3.10 or higher
- Flask
- astor
- python-dotenv
- Anthropics Python Client

---

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-repo/python-code-anonymizer.git
   cd python-code-anonymizer
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the `.env` file**:
   Create a `.env` file in the root directory and add your Anthropic API key:
   ```
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Access the app**:
   Open a web browser and navigate to `http://127.0.0.1:5000/`.

---

## Usage

![ano_full_app](https://github.com/user-attachments/assets/8a2a7f17-e5d1-4ad1-bfce-69b00c24f5af)

### Web Interface

1. **Input Python Code and Prompt**: Enter Python code and/or a prompt in the provided fields.
2. **Submit**: Click the "Anonymize and Send" button to:
   - Anonymize the code and prompt.
   - Send the anonymized content to the external API.
   - View the anonymized content, API response, and reconstructed response.

3. **View Results**:
   - **Anonymized Code**: Python code with anonymized identifiers.
   - **Anonymized Prompt**: Prompt with anonymized terms based on the code mappings.
   - **API Response**: Raw response from the external API.
   - **Rebuilt Response**: Original response reconstructed using the anonymization mappings.

---

## File Structure

- `app.py`: Flask application handling web requests and responses.
- `anonymize.py`: Contains logic for anonymizing Python code and prompts, and rebuilding API responses.
- `key.py`: Manages secure retrieval of the API key from the `.env` file.
- `anthropic_api_call.py`: Handles communication with the external API.
- `templates/index.html`: HTML for the web interface.
- `static/scripts.js`: JavaScript for UI interactivity and API integration.
- `static/styles.css`: Styling for the web interface.

---

## Limitations

- **Python-Only**: This app is designed to process Python code exclusively. Other programming languages are not supported.
- **External API Dependency**: Requires a valid API key and access to the Anthropic API for functionality.

---

## Example Workflow

1. **Input Python Code**:
   ```python
   def greet(name):
       return f"Hello, {name}!"
   ```

2. **Input Prompt**:
   ```
   What does the `greet` function do?
   ```

3. **Anonymized Output**:
   Code:
   ```python
   def function0(var0):
       return f"Hello, {var0}!"
   ```
   Prompt:
   ```
   What does the `function0` function do?
   ```

4. **API Response**: Processed response from the external API.
5. **Rebuilt Response**:
   ```
   The greet function returns a greeting message for the given name.
   ```

---

## Contributing

Feel free to fork the repository, enhance the project, and submit pull requests.

---
