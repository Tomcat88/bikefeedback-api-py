from math import sin, cos, sqrt, atan2, radians
from datetime import datetime, timedelta


def timed_cache(seconds=300):
    def _timed_cache(func):
        cache = {}
        td = timedelta(seconds=seconds)

        def decorated(*args):
            now = datetime.now()
            if args in cache:
                (entry_invalidation_time, result) = cache[args]
                if now >= entry_invalidation_time:
                    del cache[args]
                    val = func(*args)
                    cache[args] = (now + td, val)
                    return val
                else:
                    return result
            else:
                val = func(*args)
                cache[args] = (now + td, val)
                return val

        return decorated

    return _timed_cache


# approximate radius of earth in km
R = 6373.0


def coord_distance(location1, location2):
    """
    Returns the distance in km between
    two coordinates
    """

    lat1 = radians(abs(location1["lat"]))
    lat2 = radians(abs(location2["lat"]))
    lng1 = radians(abs(location1["lng"]))
    lng2 = radians(abs(location2["lng"]))

    dlng = lng2 - lng1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlng / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c


def find_nearest(stations, user_latitude, user_longitude):
    return min(
        stations,
        key=lambda s: coord_distance(
            {'lat': user_latitude, 'lng': user_longitude},
            {'lat': s.lat, 'lng': s.lng}
        )
    )
