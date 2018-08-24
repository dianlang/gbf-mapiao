# usage

## get bookmaker data

```python
import requests
import datetime
import pytz
import pprint
timezone = pytz.timezone('Asia/Shanghai')
start_time = datetime.datetime(2018, 5, 30, 6, 0, 0, tzinfo=timezone)
end_time = datetime.datetime(2018, 5, 30, 11, 30, 0, tzinfo=timezone)
start_time = int(start_time.timestamp())
end_time = int(end_time.timestamp())
r = requests.get('https://granbluefantasy.trim21.cn/api/v0.1/bookmaker?start={}&end={}'
                 .format(start_time, end_time))
pprint.pprint(r.json())
```

start_time and end_time should be standard unix timestamp.

## get individual rank history data

```python
import requests
import pprint

user_id = 'id you want to search'
r = requests.get('https://granbluefantasy.trim21.cn/api/v0.1/teamraid038/individual', {'user_id': user_id})
pprint.pprint(r.json())
```

## Cron

you need to install `pypiwin32` when you try to get cookies from Chrome on windows.

`cron/rank/individual.py` is an example for fetching individual rank.

`cron/bookmaker.py` is an example for fetching bookmaker data.

## Deploy

首先安装 
- python >= 3.6.5
- mongodb on default port

启动mongodb, 进入项目路径后`pip install -r requirements.txt`, 安装完所有的依赖.

整个项目分为两部分, server和cron

请先把项目clone到本地, 安装`pywin32`, 修改`cron/config.py`中的`profile`指定你要使用的对应的chrome的profile, 修改 `cron/vars.py`中的`teamraid`变量 , 比如2018年8月24号这次团战是 `'teamraid040'` 这个值会出现在古战场首页的网页链接中.

常识运行`cron/bookmaker.py`, 会根据对应设置的profile在`cron`文件夹下生成`cron/cookie.json`, 如果
 如果成功抓取到了数据存入数据库, 把cron文件夹复制到服务器上, 设置对应的crontab让其抓取数据.

 server文件夹不需要做修改(如果你的mongodb是运行在默认端口上), 安装好依赖后直接`python3 app.py`启动服务器, 默认会运行在6001端口.


## About data

If you just want to get all data, just Email [trim21me@hotmail.com](mailto:trim21me@hotmail.com). Do not crawl from api.
