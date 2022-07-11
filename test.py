import csv
import io

import aiofiles
import aiohttp
import asyncio
import requests
import json

from aiohttp import web
from flask import ctx
from requests import auth

height_list = []
weight_list = []
CHARACTERISTICS_API = 'https://drive.google.com/uc?export=download&id=1yM0a4CSf0iuAGOGEljdb7qcWyz82RBxl'

response = requests.get(CHARACTERISTICS_API)
csv_data = io.StringIO(response.text)
reader = csv.DictReader(csv_data, delimiter=',')
for row in reader:
    height_list.append(float(row[' "Height(Inches)"']))
    weight_list.append(round(float(row[' "Weight(Pounds)"']), 1))
average_height = round(((max(height_list) + min(height_list)) / 2) * 2.54, 2)
average_weight = round(((max(weight_list) + min(weight_list)) / 2) / 2.2046, 2)

print(average_height)
print(average_weight)
