import logging
import os
import re
from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import GPT2LMHeadModel, GPT2Tokenizer

logging.getLogger('transformers').setLevel(logging.ERROR)

gpt2model = "distilgpt2"

app = Flask(__name__)

# Load pre-trained model
tokenizer = GPT2Tokenizer.from_pretrained(gpt2model, cache_dir='./models')
model = GPT2LMHeadModel.from_pretrained(gpt2model, cache_dir='./models')

cors_origins = os.getenv('CORS_ORIGINS').split(',')
cors = CORS(app, resources={r"/generate": {"origins": cors_origins}}, supports_credentials=True)
@app.before_request
def before_request():
    # Ignore authentication for OPTIONS requests
    if request.method != 'OPTIONS':
        # Check authorization key
        if request.headers.get('authorization') != os.getenv('AUTHORIZATION_KEY'):
            return 'Unauthorized', 401

@app.route('/generate', methods=['POST'])
def generate_text():
    data = request.get_json()
    input_text = data.get('input')

    # Encode input context
    encoded_input = tokenizer.encode_plus(input_text, return_tensors='pt')

    # Generate a single token
    output = model.generate(encoded_input['input_ids'], 
                            repetition_penalty=1.2,  # higher penalty encourages model to avoid repeating itself
                            max_length=len(encoded_input['input_ids'][0])+1, 
                            temperature=0.5,  # lower temperature
                            top_k=30,  # add top-k sampling
                            top_p=0.98,  # add top-p sampling
                            num_return_sequences=1,
                            do_sample=True,
                            attention_mask=encoded_input['attention_mask'])

    # Decode the generated token
    output_token = tokenizer.decode(output[0][-1], skip_special_tokens=True)

        # Replace multiple newlines with a single newline
    output_token = re.sub('\n+', '\n', output_token)

    return jsonify({'output': output_token})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

