from flask import Flask, request, jsonify
import subprocess
import os
import random

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/random_numbers')
def random_numbers():
    numbers = [random.randint(1, 10) for _ in range(10)]
    return ', '.join(str(num) for num in numbers)


@app.route('/train_model', methods=['POST'])
def fine_tune_model():
    model_name = request.args.get('model_name')
    openai_api_key = request.args.get('openai_api_key')
    file = request.files['file']
    
    # Save the JSONL file to the server
    file.save('data.jsonl')
    
    # Set OPENAI_API_KEY environment variable
    set_command =  f"set OPENAI_API_KEY={openai_api_key}"
    
    # Prepare the command
    train_command = f"openai fine_tunes.create -t data.jsonl -m {model_name}"
    
    try:
        # Execute the command and capture the output
        output = subprocess.check_output(train_command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        
        return jsonify({'message': 'Fine-tuning process initiated.', 'output': output}), 200
    
    except subprocess.CalledProcessError as e:
        return jsonify({'message': 'Error occurred during fine-tuning.', 'output': e.output}), 500

if __name__ == '__main__':
    app.run()