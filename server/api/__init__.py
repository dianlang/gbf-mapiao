import time
from typing import List

import motor.motor_asyncio
from aiohttp import web

from utils import MissingInputException, check_and_covert_input, match_info_from_dict


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


async def teamraidIndividualRankV2(request: web.Request, ):
    mongo = request.app.mongo  # type: motor.motor_asyncio.AsyncIOMotorClient
    fields = [
        {'name': 'user_id', 'type': int, 'required': True, },
        {'name': 'start', 'type': int, 'required': True, },
        {'name': 'end', 'type': int, 'required': True, },
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
    user_id: int = data['user_id']
    start: int = data['start']
    end: int = data['end']
    collection = mongo.get_database('gbf').get_collection('{}_individual'.format(teamraid))  # type: motor.motor_asyncio.AsyncIOMotorCollection
    r = await collection.find_one({'_id': user_id}, {'_id': 0})
    if r:
        if r:
            return web.json_response({
                'status': 'success',
                'type'  : 'object',
                'data'  : {key: value for key, value in r.get("history", {}).items() if start < int(key) < end}
            }, headers={
                'Access-Control-Allow-Origin' : '*',
                'Access-Control-Allow-Methods': 'GET',
            })
    else:
        raise web.HTTPNotFound(content_type='application/json')


async def teamraidIndividualRankGroup(request: web.Request, ):
    mongo = request.app.mongo  # type: motor.motor_asyncio.AsyncIOMotorClient
    fields = [
        {'name': 'user_ids', 'type': list, 'required': True, },
        {'name': 'start', 'type': int, 'required': True, },
        {'name': 'end', 'type': int, 'required': True, },
    ]
    try:
        data = match_info_from_dict(await request.json(), fields)

        teamraid = check_and_covert_input(request,
                                          {'name': 'teamraid', 'type': str, 'required': True},
                                          'match_info')['teamraid']
        user_ids: List[int] = data['user_ids']
        user_ids = [int(x) for x in user_ids]

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
    collection = mongo.get_database('gbf').get_collection('{}_individual'.format(teamraid))  # type: motor.motor_asyncio.AsyncIOMotorCollection
    r = await collection.find({'_id': {'$in': user_ids}}).to_list(50)
    returned_data = {}
    user_ids = [str(x) for x in user_ids]

    for user in r:
        history = {key: value for key, value in user.get("history", {}).items() if start <= int(key) <= end}

        returned_data[str(int(user['_id']))] = {
            'user_id': int(user['_id']),
            'history': history or None,
        }

    for _id in user_ids:
        if _id not in returned_data:
            returned_data[_id] = {
                'user_id': int(_id),
                'history': None
            }

    if returned_data:
        return web.json_response({
            'status': 'success',
            'type'  : 'object',
            'data'  : returned_data
        }, headers={
            'Access-Control-Allow-Origin' : '*',
            'Access-Control-Allow-Methods': 'GET',
        })
    else:
        raise web.HTTPNotFound(content_type='application/json')



routes = [
    web.get('/api/v0.1/bookmaker', bookmakerRaidHandle),
    web.get('/api/v0.1/{teamraid}/individual', teamraidIndividualRank, name='teamraid_individual'),
    web.get('/api/v0.2/{teamraid}/individual', teamraidIndividualRankV2, name='teamraid_individual_v2'),
    web.post('/api/v0.1/{teamraid}/group/individual', teamraidIndividualRankGroup, name='teamraid_individual_group'),
]
