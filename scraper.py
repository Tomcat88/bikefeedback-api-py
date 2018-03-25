import urllib.request
import logging as log
import os
import re

from utils import timed_cache
from collections import namedtuple

DEVELOPMENT = os.getenv('BIKE_FEEDBACK_DEV', "True") == "True"
page_name = os.environ.get('BIKE_PAGE')

MARKER_REGEX = "GoogleMap.addMarker\\((.*)\\);"
TD_REGEX = "\<td\>(\d+)\<\/td\>"
STRONG_REGEX = "\<strong\>(\d+) - .*\<\/strong\>"

Station = namedtuple('Station', ['icon',
                                 'lat',
                                 'lng',
                                 'code',
                                 'name',
                                 'bikes',
                                 'ebikes',
                                 'racks'])


def get_bike_page():
    if page_name is None:
        log.error("BIKE_PAGE not found, skipping...")
        return None
    req = urllib.request.Request(
        page_name,
        data=None,
        headers={
            'User-Agent': '''Mozilla/5.0 (X11; Linux x86_64; rv:57.0)
                             Gecko/20100101 Firefox/57.0'''
        }
    )
    with urllib.request.urlopen(req) as page:
        return page.read().decode('utf-8')


def get_dev_page():
    with open('./test_map.html') as f:
        return f.read()


@timed_cache(seconds=120)
def scrape_bikes():
    log.info("Scraping bikes...")
    content = get_dev_page() if DEVELOPMENT else get_bike_page()
    log.debug(type(content))
    if content is None:
        log.info("Could not fetch bike content, skipping...")
        return
    markers = re.findall(MARKER_REGEX, content)
    log.info("Found %s markers" % len(markers))
    stations = []
    for m in markers:
        station = [s.replace("'", "")
                   .replace("\\r\\n", "")
                   .strip() for s in m.split(',')]
        html = station[4].encode('utf-8').decode('unicode_escape')
        tds = re.findall(TD_REGEX, html)
        strong = re.search(STRONG_REGEX, html)
        stations.append(Station(station[0],
                                float(station[1]),
                                float(station[2]),
                                int(strong.group(1)),
                                station[3],
                                int(tds[0]),
                                int(tds[2]),
                                int(tds[1])))

    return stations
