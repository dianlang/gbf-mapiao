import time

import motor.motor_asyncio
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


async def teamraidIndividualRank(request: web.Request, ):
    mongo = request.app.mongo  # type: motor.motor_asyncio.AsyncIOMotorClient
    fields = [
        {'name': 'user_id', 'type': int, 'required': False, },
        {'name': 'rank', 'type': int, 'required': False, },
    ]
    try:
        data = check_and_covert_input(request, fields, 'query')
        teamraid = check_and_covert_input(request,
                                          {'name': 'teamraid', 'type': str, 'required': True},
                                          'match_info')['teamraid']
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
    _id: int = data.get('user_id', None)
    rank: int = data.get('rank', None)
    collection = mongo.get_database('gbf').get_collection('{}_individual'.format(teamraid))  # type: motor.motor_asyncio.AsyncIOMotorCollection

    r = None
    if _id:
        r = await collection.find_one({'_id': _id}, {'_id': 0})
    if rank:
        r = await collection.find_one({'_id': 'rank_{}'.format(rank)}, {'_id': 0})
    if r:
        return web.json_response({
            'status': 'success',
            'type'  : 'object',
            'data'  : r.get("history", {})
        }, headers={
            'Access-Control-Allow-Origin' : '*',
            'Access-Control-Allow-Methods': 'GET',
        })
    else:
        raise web.HTTPNotFound(content_type='application/json')


routes = [
    web.get('/api/v0.1/bookmaker', bookmakerRaidHandle),
    web.get('/api/v0.1/{teamraid}/individual', teamraidIndividualRank, name='teamraid_individual')
]
