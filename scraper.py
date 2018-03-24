import urllib.request
import logging as log
import os
import re

page_name = os.environ.get('BIKE_PAGE')

MARKER_REGEX = "GoogleMap.addMarker\\((.*)\\);"


def get_bike_page():
    if page_name is None:
        log.error("BIKE_PAGE not found, skipping...")
        return None
    with urllib.request.urlopen(page_name) as page:
        return page.read().decode('utf-8')


def scrape_bikes():
    log.info("Scraping bikes...")
    content = get_bike_page()
    log.debug(type(content))
    if content is None:
        log.info("Could not fetch bike content, skipping...")
        return
    markers = re.findall(MARKER_REGEX, content)
    log.info("Found %s markers" % len(markers))
    #for marker in markers
    #    log.info(marker)
