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
    if teamraid == 'teamraid039':
        raise web.HTTPNotFound(reason='尚未录入数据')
    if name or _id:
        con = {}
        if name:
            con['name'] = name
        elif _id:
            con['id'] = _id
        r = await request.app.mongo.gbf.get_collection(teamraid).find_one(con, {'_id': 0})
        if not r:
            raise web.HTTPNotFound(reason='暂无相应数据')
    else:
        r = None
    return {'r': r, 'teamraid': teamraid}


routes = [
    web.get('/render/bookmaker/today', bookmakerTodayHanle),
    web.get('/render/{teamraid}/crew', teamRaidCrewHandle)
]
