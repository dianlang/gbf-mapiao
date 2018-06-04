import asyncio
import json
import pathlib
from os import path

import aiohttp
import aiohttp_jinja2
import jinja2
from aiohttp import web
from db import mongo

from api import routes as apiRoutes
from render import routes as renderRoutes

base_dir = pathlib.Path(path.dirname(__file__))


@web.middleware
async def error_middleware(request: web.Request, handler):
    try:
        response = await handler(request)
        return response
    except web.HTTPError as e:
        status = e.status_code
        message = e.reason
        if 'html' in request.headers.get('accept'):
            return aiohttp_jinja2.render_template('error/404.html', request, {'error': message, })
        else:
            return web.json_response({'error': message, 'status_code': status}, status=status)


def _raise(excep):
    raise excep


def create_app(loop=None):
    app = web.Application(loop=loop, middlewares=[error_middleware, ])
    app.mongo = mongo
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(str(base_dir / 'templates')))
    app.add_routes([
        web.get('/robots.txt', lambda x: web.Response(text='User-agent: *\nDisallow: /teamraid038/crew/')),
        web.get('/', lambda request: aiohttp_jinja2.render_template('index.html', request, {})),
        web.get('/teamraid038/crew', lambda request: _raise(web.HTTPFound('/render' + request.path_qs))),
    ])
    app.add_routes(renderRoutes)
    app.add_routes(apiRoutes)
    print('create app', flush=True)
    return app


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    web.run_app(create_app(loop=loop), port=6001)
