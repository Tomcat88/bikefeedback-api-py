from periodic import periodic
from flask import Flask
import logging as log
import telegramclient
import scraper
import sched
import time
import json

logFormatter = log.Formatter("%(asctime)s [%(levelname)-5.5s] %(message)s")

app = Flask(__name__)


@app.route("/")
def hello():
    stations = scraper.scrape_bikes()
    for s in stations:
        log.info(s)

    return "Hello World"


def configure_logger():
    rootLogger = log.getLogger()

    fileHandler = log.FileHandler("bikefeedback.log")
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)

    consoleHandler = log.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)

    rootLogger.setLevel("DEBUG")


def configure_scheduler():
    s = sched.scheduler(time.time, time.sleep)
    periodic(s, 10, fetch_updates)
    s.run()


def fetch_updates():
    log.info("Fetching updates")
    updates = telegramclient.get_updates()
    log.info(updates)


if __name__ == "__main__":
    configure_logger()
    configure_scheduler()
#    app.run()
