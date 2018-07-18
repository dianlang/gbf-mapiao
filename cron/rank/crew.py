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


import time
import datetime
import grequests

import html.parser


def main():
    s = initSession()
    urls = ['http://game.granbluefantasy.jp/{teamraid}/ranking_guild/detail/{index}/0'.format(teamraid=teamraid, index=index) for index in range(1, 2017)]
    rs = (grequests.get(u, session=s, stream=False) for u in urls)
    results = grequests.map(rs, size=40)
    now = int(time.time())
    c = db.get_collection(teamraid)
    for r in results:
        try:
            res = r.json()
            for item in res['list']:
                item['time'] = now
                item['name'] = html.parser.unescape(item['name'])
            c.insert_many(res['list'])
        except Exception as e:
            raise e
            print(r.text)


if __name__ == '__main__':
    print('======fetching individual ranking======')
    main()
    print('======{}======'.format(datetime.datetime.now()))
