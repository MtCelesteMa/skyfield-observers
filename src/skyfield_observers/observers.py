# Observers

import skyfield.api
import skyfield.almanac


class Observer:
    def __init__(self, eph, name=None, lat=0.0, lon=0.0, elev=0.0):
        self.name = name

        self.eph = eph
        self.loc = None
        self.set_location(lat, lon, elev)

        self.ts = skyfield.api.load.timescale()
        self.t = self.ts.now()

    def set_location(self, lat=0.0, lon=0.0, elev=0.0):
        self.loc = self.eph['earth'] + skyfield.api.wgs84.latlon(lat, lon, elev)

    def set_datetime(self, dt):
        self.t = self.ts.from_datetime(dt)

    def observe(self, body):
        return self.loc.at(self.t).observe(body)

    def search_rise_set(self, body, sr_start, sr_end, horizon_offset=-0.57, radius=0):
        event_fn = skyfield.almanac.risings_and_settings(self.eph, body, self.loc, horizon_offset, radius)
        rs_times, rs_ids = skyfield.almanac.find_discrete(sr_start, sr_end, event_fn)
        rs_positions = self.loc.at(rs_times).observe(body)
        return rs_ids, rs_times, rs_positions

    def search_transits(self, body, sr_start, sr_end):
        event_fn = skyfield.almanac.meridian_transits(self.eph, body, self.loc)
        t_times, t_ids = skyfield.almanac.find_discrete(sr_start, sr_end, event_fn)
        t_positions = self.loc.at(t_times).observe(body)
        return t_ids, t_times, t_positions
