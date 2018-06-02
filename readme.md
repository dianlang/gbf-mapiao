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