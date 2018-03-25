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
