import time

from aiohttp import web

from utils import MissingInputException, check_and_covert_input


async def bookmakerRaidHandle(request: web.Request, ):
    mongo = request.app.mongo
    fields = [
        {'name': 'start', 'type': int, 'required': True, },
        {'name': 'end', 'type': int, 'required': False, 'default': int(time.time())}
    ]
    try:
        data = check_and_covert_input(request, fields, 'query')
    except MissingInputException as e:
        return web.json_response({
            'status' : 'error',
            'message': str(e),
        }, status=400)
    except ValueError as e:
        return web.json_response({
            'status' : 'error',
            'message': str(e),
        }, status=400)
    start: int = data['start']
    end: int = data['end']
    print(start, end)
    r = await mongo.gbf.bookmaker.find({'time': {'$gte': start, '$lte': end}}, {'_id': 0}) \
        .sort([('time', 1)]).limit(100).to_list(100)
    return web.json_response({
        'status': 'success',
        'type'  : 'list',
        'length': len(r),
        'data'  : r
    }, headers={
        'Access-Control-Allow-Origin' : '*',
        'Access-Control-Allow-Methods': 'GET',
    })


routes = [
    web.get('/api/v0.1/bookmaker', bookmakerRaidHandle)
]
