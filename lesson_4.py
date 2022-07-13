import random

import requests
from flask import Flask
from webargs import fields
from webargs.flaskparser import use_args

from constants import PASSWORD_CHARACTERS
from settings import ROOT_PATH

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/greetings')
def greetings():
    return 'Hi'


@app.route('/path/sub-path/etn')
def etn():
    return ';)))'


@app.route('/hi/<name>/<int:age>')
def hi(name: str, age: int):
    return f"Hi {name}. I'm {age} old."


@app.route('/hello')
@use_args({"name": fields.Str(required=True), "age": fields.Int(required=True)}, location="query")
def hello(args):
    return f'Hello {args["name"]}. I\'m {args["age"]} old.'


@app.route('/example-file')
def example_file():
    return ROOT_PATH.joinpath('requirements.txt').read_text()


@app.route('/example-request')
def example_request():
    response = requests.get(url='https://example.com')
    return str(response.status_code)


@app.route('/generate-password/<int:password_length>')
def generate_password(password_length: int):
    """Generate password.
    """
    password_as_list = [random.choice(PASSWORD_CHARACTERS) for _ in range(password_length)]
    random.shuffle(password_as_list)
    password = ''.join(password_as_list)
    return f"""<p>Length:{len(password)}:</p>
    <p>{password}</p>
"""


if __name__ == '__main__':
    app.run()
