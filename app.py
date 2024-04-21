from flask import Flask, request, jsonify
import openai  # Ensure you have openai library if you are using it within generate_response
from main import generate_response

app = Flask(_name_)

def generate_response(query, step, mode, context=""):
    # Dummy implementation of generate_response
    return f"Processed {query} with step {step} and mode {mode}, context: {context[:50]}"

@app.route('/process_query', methods=['POST'])
def process_query():
    content = request.json
    response = generate_response(content['query'], content['step'], content['mode'], content.get('context', ''))
    return jsonify(response)

if _name_ == "_main_":
    app.run(debug=True, host='0.0.0.0',port=5001)