import datetime
import pathlib
import sys
import time
from os import path

import grequests
import pytz

dir = pathlib.Path(path.dirname(__file__))
sys.path.append(str(dir.parent / 'cron'))
sys.path.append(str(dir.parent))

from mongo import db
from utils import initSession
from vars import teamraid


def main():
    s = initSession()

    urls = ['http://game.granbluefantasy.jp/{teamraid}/rest_ranking_user/detail/{index}/0'.format(
        teamraid=teamraid, index=index) for index in list(range(2999, 3001)) + list(range(4999, 5001))]
    rs = (grequests.get(u, session=s, stream=False, ) for u in urls)
    results = grequests.map(rs, size=5)
    now = int(time.time())
    c = db.get_collection('{}_individual'.format(teamraid))
    for r in results:
        try:
            print(r.headers)

            res = r.json()
            for item in res['list'].values():
                item['time'] = now
                item['point'] = int(item['point'])
                # c.update_one({'_id': int(item['user_id'])},
                #              {'$set': {'history.' + str(now): {'point': item['point'], 'rank': item['rank']}}},
                #              upsert=True)
                if int(item['rank']) in [1000, 30000, 50000, 70000, 120000]:
                    c.update_one({'_id': 'rank_{}'.format(item['rank'])},
                                 {'$set': {'history.' + str(now): {'point': item['point'], 'rank': item['rank']}}},
                                 upsert=True)
        except:
            print(r.text)


if __name__ == '__main__':
    print('======{}======'.format(datetime.datetime.now()))
    main()
    print('======{}======'.format(datetime.datetime.now()))
