# Skyfield Observers
Ephem-style observers for [Skyfield](https://rhodesmill.org/skyfield/).

## Installation
Skyfield Observers can be installed via pip using the following command:
```bash
pip install git+https://github.com/MtCelesteMa/skyfield-observers.git
```

## Examples
Create an observer at Los Angeles:
```python
import skyfield.api
import skyfield_observers

# Load ephemeris file
eph = skyfield.api.load('de421.bsp')

# Create observer
obs = skyfield_observers.Observer(eph, 'Los Angeles') # Observer name is optional and does not affect functionality

# Set observer location to Los Angeles
obs.set_location(34.0522, -118.2437, 93) # 34.0522˚N 118.2437˚W 93.0 m
```

Calculate the position of the sun in the sky at noon 2020/01/01:
```python
import datetime
import zoneinfo

# Set observer time
tz = zoneinfo.ZoneInfo('America/Los_Angeles')
dt = datetime.datetime(2020, 1, 1, 12, tzinfo=tz)
obs.set_datetime(dt)

# Calculate sun position
sun_pos = obs.observe(eph['sun'])
alt, az, distance = sun_pos.apparent().altaz()

# Print sun position
print('Altitude: {alt:.2f}, Azimuth: {az:.2f}'.format(alt=alt.degrees, az=az.degrees))
```

Calculate the time and azimuth of sunrise on 2020/01/01:
```python
# Calculate sunrise time and position
r_times, r_positions = obs.previous_risings(eph['sun'], radius=0.25)
r_time, r_position = r_times[0], r_positions[0]
r_dt = r_time.astimezone(tz)
alt, az, distance = r_position.apparent().altaz()

# Print sunrise time and position
print('Sunrise: {r_time} (Azimuth: {az:.2f})'.format(r_time=r_dt, az=az.degrees))
```
