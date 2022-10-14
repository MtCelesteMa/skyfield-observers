# Observers

import skyfield.api


class Observer:
    def __init__(self, eph, name=None, lat=0.0, lon=0.0, elev=0.0):
        self.name = name

        self.eph = eph
        self.loc = None
        self.set_location(lat, lon, elev)

        self.ts = skyfield.api.load.timescale()
        self.t = ts.now()

    def set_location(self, lat=0.0, lon=0.0, elev=0.0):
        self.loc = self.eph['earth'] + skyfield.api.wgs84.latlon(lat, lon, elev)

    def set_datetime(self, dt):
        self.t = self.ts.from_datetime(dt)

    def observe(self, body):
        return self.loc.at(self.t).observe(body)
