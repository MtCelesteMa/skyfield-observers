# Observers

import datetime

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
        self.loc = skyfield.api.wgs84.latlon(lat, lon, elev)

    def set_datetime(self, dt):
        self.t = self.ts.from_datetime(dt)

    def observe(self, body):
        return (self.eph['earth'] + self.loc).at(self.t).observe(body)

    def search_rise_set(self, body, sr_start, sr_end, horizon_offset=-0.57, radius=0):
        event_fn = skyfield.almanac.risings_and_settings(self.eph, body, self.loc, horizon_offset, radius)
        rs_times, rs_ids = skyfield.almanac.find_discrete(sr_start, sr_end, event_fn)
        rs_positions = (self.eph['earth'] + self.loc).at(rs_times).observe(body)
        return rs_ids, rs_times, rs_positions

    def previous_risings(self, body, horizon_offset=-0.57, radius=0, search_range=datetime.timedelta(days=1)):
        sr_start = self.t - search_range
        sr_end = self.t
        rs_ids, rs_times, rs_positions = self.search_rise_set(body, sr_start, sr_end, horizon_offset, radius)
        r_times, r_positions = rs_times[rs_ids == 1], rs_positions[rs_ids == 1]
        return r_times[::-1], r_positions[::-1]

    def next_risings(self, body, horizon_offset=-0.57, radius=0, search_range=datetime.timedelta(days=1)):
        sr_start = self.t
        sr_end = self.t + search_range
        rs_ids, rs_times, rs_positions = self.search_rise_set(body, sr_start, sr_end, horizon_offset, radius)
        r_times, r_positions = rs_times[rs_ids == 1], rs_positions[rs_ids == 1]
        return r_times, r_positions

    def previous_settings(self, body, horizon_offset=-0.57, radius=0, search_range=datetime.timedelta(days=1)):
        sr_start = self.t - search_range
        sr_end = self.t
        rs_ids, rs_times, rs_positions = self.search_rise_set(body, sr_start, sr_end, horizon_offset, radius)
        s_times, s_positions = rs_times[rs_ids == 0], rs_positions[rs_ids == 0]
        return s_times[::-1], s_positions[::-1]

    def next_settings(self, body, horizon_offset=-0.57, radius=0, search_range=datetime.timedelta(days=1)):
        sr_start = self.t
        sr_end = self.t + search_range
        rs_ids, rs_times, rs_positions = self.search_rise_set(body, sr_start, sr_end, horizon_offset, radius)
        s_times, s_positions = rs_times[rs_ids == 0], rs_positions[rs_ids == 0]
        return s_times, s_positions

    def search_transits(self, body, sr_start, sr_end):
        event_fn = skyfield.almanac.meridian_transits(self.eph, body, self.loc)
        t_times, t_ids = skyfield.almanac.find_discrete(sr_start, sr_end, event_fn)
        t_positions = self.loc.at(t_times).observe(body)
        return t_ids, t_times, t_positions

    def previous_transits(self, body, search_range=datetime.timedelta(days=1)):
        sr_start = self.t - search_range
        sr_end = self.t
        t_ids, t_times, t_positions = self.search_transits(body, sr_start, sr_end)
        t_times, t_positions = t_times[t_ids == 1], t_positions[t_ids == 1]
        return t_times[::-1], t_positions[::-1]

    def next_transits(self, body, search_range=datetime.timedelta(days=1)):
        sr_start = self.t
        sr_end = self.t + search_range
        t_ids, t_times, t_positions = self.search_transits(body, sr_start, sr_end)
        t_times, t_positions = t_times[t_ids == 1], t_positions[t_ids == 1]
        return t_times, t_positions

    def previous_antitransits(self, body, search_range=datetime.timedelta(days=1)):
        sr_start = self.t - search_range
        sr_end = self.t
        t_ids, t_times, t_positions = self.search_transits(body, sr_start, sr_end)
        a_times, a_positions = t_times[t_ids == 0], t_positions[t_ids == 0]
        return a_times[::-1], a_positions[::-1]

    def next_antitransits(self, body, search_range=datetime.timedelta(days=1)):
        sr_start = self.t
        sr_end = self.t + search_range
        t_ids, t_times, t_positions = self.search_transits(body, sr_start, sr_end)
        a_times, a_positions = a_times[t_ids == 0], a_positions[t_ids == 0]
        return a_times, a_positions
