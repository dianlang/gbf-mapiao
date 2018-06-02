import time
import datetime
import grequests
from mongo import db
from utils import initSession
from vars import teamraid
import html.parser


def main():
    s = initSession()
    urls = ['http://game.granbluefantasy.jp/{teamraid}/ranking_guild/detail/{index}/0'.format(teamraid=teamraid, index=index) for index in range(1, 2015)]
    rs = (grequests.get(u, session=s, stream=False) for u in urls)
    results = grequests.map(rs, size=40)
    now = int(time.time())
    for r in results:
        try:
            res = r.json()
            c = db.get_collection('crew')
            for item in res['list'].values():
                item['time'] = now
                item['name'] = html.parser.unescape(item['name'])
            c.insert_many(res['list'].values())
        except:
            print(r.text)


if __name__ == '__main__':
    print('======fetching individual ranking======')
    main()
    print('======{}======'.format(datetime.datetime.now()))
