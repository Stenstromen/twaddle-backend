from flask import Flask, request, jsonify
from transformers import GPT2LMHeadModel, GPT2Tokenizer

app = Flask(__name__)

# Load pre-trained model
tokenizer = GPT2Tokenizer.from_pretrained('gpt2-large')
model = GPT2LMHeadModel.from_pretrained('gpt2-large')

@app.route('/generate', methods=['POST'])
def generate_text():
    data = request.get_json()
    input_text = data.get('input')

    # Encode input context
    encoded_input = tokenizer.encode_plus(input_text, return_tensors='pt')

    # Generate a single token
    output = model.generate(encoded_input['input_ids'], 
                            max_length=len(encoded_input['input_ids'][0])+1, 
                            temperature=0.7, 
                            num_return_sequences=1,
                            do_sample=True,
                            attention_mask=encoded_input['attention_mask'])

    # Decode the generated token
    output_token = tokenizer.decode(output[0][-1], skip_special_tokens=True)

    return jsonify({'output': output_token})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

