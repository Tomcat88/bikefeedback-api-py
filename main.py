from flask import Flask
import logging
import scraper
logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s] %(message)s")

app = Flask(__name__)


@app.route("/")
def hello():
    scraper.scrape_bikes()
    return "Hello World"


def configure_logger():
    rootLogger = logging.getLogger()

    fileHandler = logging.FileHandler("bikefeedback.log")
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)

    rootLogger.setLevel("DEBUG")


if __name__ == "__main__":
    configure_logger()
    app.run()
