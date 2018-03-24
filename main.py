from flask import Flask
import logging as log
import scraper
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


if __name__ == "__main__":
    configure_logger()
    app.run()
