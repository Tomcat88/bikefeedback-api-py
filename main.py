from periodic import periodic
import updates_dispatcher
import logging as log
import telegramclient
import sched
import time

logFormatter = log.Formatter("%(asctime)s [%(levelname)-5.5s] %(message)s")


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
    updates_dispatcher.dispatch(updates)


if __name__ == "__main__":
    configure_logger()
    try:
        configure_scheduler()
    except Exception as e:
        log.error("Error while executing scheduler periodic %s", str(e))
