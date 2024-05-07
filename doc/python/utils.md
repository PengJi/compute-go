### convert nanoseconds to human-readable
```py
>>> from datetime import datetime
>>> dt = datetime.fromtimestamp(1360287003083988472 / 1000000000)
>>> dt
datetime.datetime(2013, 2, 7, 17, 30, 3)

>>> s = dt.strftime('%Y-%m-%d %H:%M:%S')
>>> s
'2013-02-07 17:30:03'

>>> s += '.' + str(int(1360287003083988472 % 1000000000)).zfill(9)
>>> s
'2013-02-07 17:30:03.083988472'

>>> dt.strftime('%Y-%m-%dT%H:%M:%S.%f')
'2013-02-07T17:30:03.083988'
```

### calculate elapsed time
```py 
import monotonic
start_time = monotonic.monotonic()
elapsed_time = int(monotonic.monotonic() - start_time)
```
