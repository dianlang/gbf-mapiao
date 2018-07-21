import time
import urllib.parse
# import win32crypt
import json
import datetime

from bs4 import BeautifulSoup

from mongo import bookmaker
from utils import initSession
from vars import cron_dir, teamraid


def main():
    s = initSession()
    r = s.get('http://game.granbluefantasy.jp/quest/content/scene')
    print(r.text)
    # with open(str(cron_dir / 'cookie.json'), 'w+', encoding='utf8') as f:
    #     json.dump({o.name: o.value for o in s.cookies}, f)
    # try:
    #     res = r.json()
    #
    #     soup = BeautifulSoup(urllib.parse.unquote(res['data']), 'html.parser')
    #     data = {
    #         'north': int(soup.find('div', class_='lis-area area1').div.decode_contents().replace(',', '')),
    #         'west' : int(soup.find('div', class_='lis-area area2').div.decode_contents().replace(',', '')),
    #         'east' : int(soup.find('div', class_='lis-area area3').div.decode_contents().replace(',', '')),
    #         'south': int(soup.find('div', class_='lis-area area4').div.decode_contents().replace(',', '')),
    #         'time' : int(time.time())
    #     }
    #
    #     result = bookmaker.insert_one(data)
    #     print(data)
    #     print(result)
    # except:
    #     print(r.text)


if __name__ == '__main__':
    main()
    print('======{}======'.format(datetime.datetime.now()))
