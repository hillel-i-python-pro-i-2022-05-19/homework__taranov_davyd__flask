import csv
import io
import sqlite3

import requests
from faker import Faker
from flask import Flask
from webargs import fields
from webargs.flaskparser import use_args

from constants import SPACE_API, CHARACTERISTICS_URL
from settings import ROOT_PATH, DB_PHONES_PATH

app = Flask(__name__)
faker = Faker()


@app.route('/')
def hello_world():
    return '<h1>Hello World!</h1>'


@app.route('/read-README')
def read_lesson() -> str:
    return ROOT_PATH.joinpath('README.md').read_text()


@app.route('/read-README-classical-method')
def read_README() -> str:
    with open('README.md', 'r') as file:
        data = file.readlines()
    return str(data)


@app.route('/generate-users/')
@use_args({'amount': fields.Int(missing=10)}, location="query")
def generate_users(args: int) -> str:
    users_list = [faker.unique.first_name() for _ in range(args['amount'])]
    formatted_users_list = [f"""<p>{user} {str(user).lower()}@mail.co</p>""" for user in users_list]
    new_users = ''.join(formatted_users_list)
    return new_users


@app.route('/astronauts-with-requests')
def astronauts_with_requests() -> str:
    response = requests.get(SPACE_API)
    result = response.json()
    people_list = ''.join([f"<li>{people['name']}</li>" for people in result["people"]])
    return f"""<h1>Количество астронавтов: {result['number']}</h1>
    <ul>Имена: {people_list}</ul>
"""


@app.route('/characteristics')
def characteristics() -> str:
    height_list = []
    weight_list = []
    response = requests.get(CHARACTERISTICS_URL)
    csv_data = io.StringIO(response.text)
    reader = csv.DictReader(csv_data, delimiter=',')
    for row in reader:
        height_list.append(float(row[' "Height(Inches)"']))
        weight_list.append(float(row[' "Weight(Pounds)"']))
    average_height = round(((max(height_list) + min(height_list)) / 2) * 2.54, 2)
    average_weight = round(((max(weight_list) + min(weight_list)) / 2) / 2.2046, 2)
    return f"""<p>Средний вес: {average_weight} кг</p>
    <p>Средний рост: {average_height} см</p>    
"""


class Connection:
    def __init__(self):
        self._connection: sqlite3.Connection | None = None

    def __enter__(self):
        self._connection = sqlite3.connect(DB_PHONES_PATH)
        self._connection.row_factory = sqlite3.Row
        return self._connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._connection.close()


@app.route('/phones/create/')
@use_args({"contactName": fields.Str(required=True), "phoneValue": fields.Int(required=True)}, location="query")
def phones__create(args):
    with Connection() as connection:
        with connection:
            connection.execute(
                'INSERT INTO phones (contactName, phoneValue) VALUES (:contactName, :phoneValue);',
                {'contactName': args['contactName'], 'phoneValue': args['phoneValue']}
            )
    return 'OK'


@app.route('/phones/read/')
def phones__read_all():
    with Connection() as connection:
        phones = connection.execute("SELECT * FROM phones;").fetchall()
    return '<br>'.join([f'''{phone['phoneID']}: {phone['contactName']} - {phone['phoneValue']}''' for phone in phones])


@app.route('/phones/update/<int:phoneID>')
@use_args({"phoneValue": fields.Int(required=True), "contactName": fields.Str(required=True)}, location="query")
def phones__update(args, phoneID):
    with Connection() as connection:
        with connection:
            connection.execute(
                'UPDATE phones '
                'SET phoneValue=:phoneValue, contactName=:contactName '
                'WHERE phoneID=:phoneID;',
                {'phoneValue': args['phoneValue'], 'contactName': args['contactName'], 'phoneID': phoneID}
            )
    return 'OK'


@app.route('/phones/delete/<int:phoneID>')
def phones__delete(phoneID):
    with Connection() as connection:
        with connection:
            connection.execute(
                'DELETE FROM phones WHERE (phoneID=:phoneID);',
                {'phoneID': phoneID}
            )
    return 'OK'


if __name__ == '__main__':
    app.run()
