import datetime
import aiohttp.web
import aiohttp_jinja2
import pytz
from aiohttp import web
from db import mongo


@aiohttp_jinja2.template('crew/bookmaker/chart.html')
async def bookmakerTodayHanle(request: aiohttp.web.Request, ):
    # today = datetime.datetime.today()
    start = datetime.datetime(2018, 5, 30, tzinfo=pytz.timezone('Asia/Shanghai'))
    end = start + datetime.timedelta(hours=24)
    url = '/api/v0.1/bookmaker?start={start}&end={end}' \
        .format(start=int(start.timestamp()), end=int(end.timestamp()))
    return {'url': url}


@aiohttp_jinja2.template('crew/result.html')
async def teamRaidCrewHandle(request: aiohttp.web.Request, ):
    name = request.query.get('name', None)
    _id = request.query.get('id', None)
    teamraid = request.match_info.get('teamraid', None)
    if teamraid not in ['teamraid038', 'teamraid039']:
        raise web.HTTPNotFound(reason='古战id错误')
    if name:
        r = await request.app.mongo.gbf.get_collection(teamraid).find_one({'name': name}, {'_id': 0})
    elif _id:
        r = await request.app.mongo.gbf.get_collection(teamraid).find_one({'id': _id}, {'_id': 0})
    else:
        if teamraid == 'teamraid039':
            raise web.HTTPNotFound(reason='暂无相应数据或是尚未录入数据')
        raise web.HTTPNotFound(reason='暂无相应数据')
    return {'r': r, 'name': name, '_id': _id, 'teamraid': teamraid}


routes = [
    web.get('/render/bookmaker/today', bookmakerTodayHanle),
    web.get('/render/{teamraid}/crew', teamRaidCrewHandle)
]
