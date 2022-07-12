import asyncio
import json

import aiohttp
from aiohttp import web
from flask import Flask

from app import SPACE_API


# app = Flask(__name__)





# @app.route('/astronauts-with-aiohttp')
# async def astronauts_with_aiohttp():
#     async with aiohttp.ClientSession() as session:
#         async with session.get(SPACE_API) as response:
#             return f'Количество космонавтов в данный момент:'


# app = web.Application()
# app.add_routes([web.get('/', astronauts_with_aiohttp),
#                 web.get('/{name}', astronauts_with_aiohttp)])



# if __name__ == '__main__':
#     web.run_app(app)



# @app.route('/astronauts-with-aiohttp')
# async def astronauts_with_aiohttp():
#     async with aiohttp.ClientSession() as session:
#         async with session.get(SPACE_API) as response:
#             return f'Количество космонавтов в данный момент:'

# loop = asyncio.get_event_loop()
# loop.run_until_complete(astronauts_with_aiohttp())