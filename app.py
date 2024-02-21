import os
import warnings
import torch
import logging
from flask import Flask, request
from flask_socketio import SocketIO, emit
from transformers import GPT2LMHeadModel, GPT2Tokenizer

authorization_key = os.getenv('AUTHORIZATION_KEY')
cors_origins = os.getenv('CORS_ORIGINS')
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins=cors_origins)

gpt2model = "distilgpt2"
tokenizer = GPT2Tokenizer.from_pretrained(gpt2model, cache_dir='./models')
model = GPT2LMHeadModel.from_pretrained(gpt2model, cache_dir='./models')

@socketio.on('connect')
def connect():
    auth_token = request.args.get('auth')
    if not auth_token or auth_token != authorization_key:
        return False

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('generate')
def handle_generate(data):
    input_text = data['input']
    input_ids = tokenizer.encode(input_text, return_tensors='pt', add_special_tokens=True)

    new_user_input_ids = input_ids

    max_length: int = data['max_length']

    print("Generating...")

    for _ in range(max_length):
        output = model.generate(new_user_input_ids, max_length=1, pad_token_id=tokenizer.eos_token_id, do_sample=True)
        
        next_token_id = output[:, -1].item()
        next_token = tokenizer.decode(next_token_id)
        
        emit('generated', {'output': next_token})
        
        if next_token_id == tokenizer.eos_token_id:
            break
        
        output_token_ids = output[:, -1].unsqueeze(-1)

        new_user_input_ids = torch.cat([new_user_input_ids, output_token_ids], dim=-1)

    print("Generation complete.")
    emit('generated', {'output': 'Generation complete.'})

warnings.filterwarnings("ignore", category=UserWarning, module="transformers")
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8080, debug=False, allow_unsafe_werkzeug=True)
