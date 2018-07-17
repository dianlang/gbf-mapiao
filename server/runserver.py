import asyncio
import pathlib
from os import path

import aiohttp
from aiohttp import web
from aiohttp_devtools.runserver import serve

base_dir = pathlib.Path(path.dirname(__file__))


async def index(request: aiohttp.web.BaseRequest):
    return web.Response(body='hello world')


def create_app(loop=None):
    app = web.Application(loop=loop)
    app.add_routes([
        web.get('/', index),
    ])
    print('create app', flush=True)
    return app

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    print('main')
    web.run_app(create_app(loop=loop), port=6001)
