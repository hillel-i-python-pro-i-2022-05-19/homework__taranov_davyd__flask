import csv
import json

import aiohttp
import asyncio
import io
import requests
from flask import Flask
from faker import Faker
from settings import ROOT_PATH, SPACE_API, CHARACTERISTICS_URL

app = Flask(__name__)
faker = Faker()



@app.route('/read-lesson')
def read_lesson() -> str:
    return ROOT_PATH.joinpath('lesson.py').read_text()


@app.route('/read-README')
def read_README() -> str:
    with open('README.md', 'r') as file:
        data = file.readlines()
    return str(data)


@app.route('/generate-users/')
def generate_users(amount: int = 100) -> str:
    users = [faker.unique.first_name() for _ in range(amount)]
    new_user = ''
    for user in users:
        new_user += f"""<p>{user} {str(user).lower()}@mail.co</p>"""
    return new_user


@app.route('/generate-users/<int:amount>')
def generate_users_by_amount(amount: int) -> str:
    return generate_users(amount)


@app.route('/astronauts-with-requests')
def astronauts_with_requests() -> str:
    response = requests.get(SPACE_API)
    result = response.json()
    names = ''
    for people in result["people"]:
        names += f"<li>{people['name']}</li>"
    return f"""<h1>Количество астронавтов: {result['number']}</h1>
    <ul>Имена: {names}</ul>
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


if __name__ == '__main__':
    app.run(debug=True)
