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

## About data

If you just want to get all data, just Email [trim21me@hotmail.com](mailto:trim21me@hotmail.com). Do not crawl from api.


"TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256:TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384:TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA:TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA:TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256:TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384:TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256:TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384:TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA:TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA:TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256:TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384:TLS_DHE_RSA_WITH_AES_128_GCM_SHA256:TLS_DHE_RSA_WITH_AES_256_GCM_SHA384:TLS_DHE_RSA_WITH_AES_128_CBC_SHA:TLS_DHE_RSA_WITH_AES_256_CBC_SHA:TLS_DHE_RSA_WITH_AES_128_CBC_SHA256:TLS_DHE_RSA_WITH_AES_256_CBC_SHA256"

ECDHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-SHA256:ECDHE-ECDSA-AES256-SHA384:DHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES128-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-SHA256:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES128-SHA256:ECDHE-RSA-AES256-SHA384