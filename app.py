from flask import Flask
import random

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/random_numbers')
def random_numbers():
    numbers = [random.randint(1, 10) for _ in range(10)]
    return ', '.join(str(num) for num in numbers)

if __name__ == '__main__':
    app.run()