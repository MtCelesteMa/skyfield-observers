# Skyfield Observers
Ephem-style observers for Skyfield.

## Installation
Skyfield Observers can be installed via pip using the following command:
```bash
pip install git+https://github.com/gerry2022153/skyfield-observers.git
```

## Examples
Calculate the position of the sun in the sky in Los Angeles at noon 2020/01/01:
```python
import datetime
import zoneinfo
import skyfield.api
import skyfield_observers

tz = zoneinfo.ZoneInfo('America/Los_Angeles')
dt = datetime.datetime(2020, 1, 1, 12, tzinfo=tz)

eph = skyfield.api.load('de421.bsp')
obs = skyfield_observers.Observer(eph, 'Los Angeles')
obs.set_location(34.0522, -118.2437, 93) # 34.0522˚N 118.2437˚W 93.0 m
obs.set_datetime(dt)
alt, az, distance = obs.observe(eph['sun']).apparent().altaz()
print('Altitude: {alt:.2f}, Azimuth: {az:.2f}'.format(alt=alt.degrees, az=az.degrees))
```
