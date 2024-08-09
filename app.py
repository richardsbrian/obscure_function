from flask import Flask, render_template, request, jsonify
from anonymize import anonymize_function, anonymize_prompt, merge_code_and_prompt, rebuild, send_prompt

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/anonymize_and_send', methods=['POST'])
def anonymize_and_send():
    code = request.form.get('code', '').strip()
    prompt = request.form.get('prompt', '').strip()

    if not code and not prompt:
        return jsonify({"error": "Please provide code, a prompt, or both."}), 400

    name_list = []
    anonymized_code = ""
    anonymized_prompt = ""

    if code:
        anonymized_code, name_list = anonymize_function(code)

    if prompt:
        anonymized_prompt = anonymize_prompt(prompt, name_list)

    merged_code_and_prompt = merge_code_and_prompt(anonymized_code, anonymized_prompt)

    try:
        response = send_prompt(merged_code_and_prompt)
        response_text = response.content[0].text
    except Exception as e:
        return jsonify({"error": f"Failed to get response: {e}"}), 500

    rebuilt_response = rebuild(response_text, name_list)

    return jsonify({
        "anonymized": merged_code_and_prompt,
        "response": response_text,
        "rebuilt_response": rebuilt_response
    })

if __name__ == "__main__":
    app.run(debug=True)
