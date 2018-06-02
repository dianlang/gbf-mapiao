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
            teamraid=teamraid, index=index) for index in range(1, 12001)]
    rs = (grequests.get(u, session=s, stream=False) for u in urls)
    results = grequests.map(rs, size=20)
    now = int(time.time())
    for r in results:
        try:
            res = r.json()
            c = db.get_collection('individual')
            for item in res['list'].values():
                item['time'] = now
            c.insert_many(res['list'].values())
        except:
            print(r.text)


if __name__ == '__main__':
    print('======fetching individual ranking======')
    today = datetime.datetime.today()
    start = datetime.datetime(today.year, today.month, today.day, 6, 0, 0, tzinfo=pytz.timezone('Asia/Shanghai'))
    while True:
        while True:
            time.sleep(3)
            step = 20 * 60
            t = step - int(datetime.datetime.now().timestamp() - start.timestamp()) % step
            sys.stdout.write('\r' + str(t) + ' ')
            sys.stdout.flush()
            if t < 10:
                time.sleep(7)
                now = datetime.datetime.now()
                if (now.hour <= 5 and now.minute < 5) or (23 <= now.hour and 30 < now.minute):
                    time.sleep(60 * 5)
                    continue
                break
        print('\r', end='')
        n = datetime.datetime.now()
        main()
        print('======{}=={}======'.format(n, datetime.datetime.now()))
