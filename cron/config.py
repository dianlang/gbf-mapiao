import os

env = os.environ.get('PROJECT_ENV') or 'server'

proxies = {}
profile = 'Default'
headerString = """
Accept           : application/json, text/javascript, */*; q=0.01
Accept-Encoding  : gzip, deflate
Accept-Language  : zh-CN,zh;q=0.9,zh-TW;q=0.8,en-US;q=0.7,en;q=0.6
Host             : game.granbluefantasy.jp
Referer          : http://game.granbluefantasy.jp/
User-Agent       : Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36
X-Requested-With : XMLHttpRequest
X-VERSION        : {version}
"""


mongo = {
    'url': 'mongodb://127.0.0.1:27017/',
    'db' : 'gbf'
}
if env == 'local':
    proxies = {'http': 'http://127.0.0.1:8123'}
    # profile = 'Profile 2'
