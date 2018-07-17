import asyncio
import json
import pathlib
from os import path
from typing import List

import aiohttp
import aiohttp_jinja2
import jinja2
from aiohttp import web
from aiohttp.web_urldispatcher import Resource

from db import mongo

from api import routes as apiRoutes
from render import routes as renderRoutes

base_dir = pathlib.Path(path.dirname(__file__))


@web.middleware
async def error_middleware(request: web.Request, handler):
    try:
        response = await handler(request)
        if request.path.startswith('/api/'):
            if 'html' in request.headers.get('accept', ''):
                response.text = json.dumps(json.loads(response.text), ensure_ascii=False, indent=2)
        return response
    except web.HTTPError as e:
        status = e.status_code
        message = e.reason
        if request.path.startswith('/api/'):
            if 'html' in request.headers.get('accept', ''):
                indent = 2
            else:
                indent = 0
            return web.Response(text=json.dumps({'error': message, 'status_code': status},
                                                ensure_ascii=False, indent=indent),
                                status=status)
        return aiohttp_jinja2.render_template('error/404.html', request, {'error': message, })


def _raise(exception: Exception):
    raise exception


def create_app(io_loop=None):
    app = web.Application(loop=io_loop, middlewares=[error_middleware, ])
    app.mongo = mongo
    aiohttp_jinja2.setup(app,
                         loader=jinja2.FileSystemLoader(str(base_dir / 'templates')),
                         enable_async=False,

                         )
    app.add_routes([
        web.get('/', lambda request: aiohttp_jinja2.render_template('index.html', request, {})),
        web.get('/robots.txt', lambda x: web.Response(text='User-agent: *\nDisallow: /teamraid038/crew/')),
        web.get('/teamraid038/crew', lambda request: _raise(web.HTTPFound('/render' + request.path_qs))),
    ])
    # r = app.router._resources  # type: List[Resource]
    app.add_routes(renderRoutes)
    app.add_routes(apiRoutes)
    print('create app', flush=True)
    return app


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    web.run_app(create_app(io_loop=loop), port=6001)
