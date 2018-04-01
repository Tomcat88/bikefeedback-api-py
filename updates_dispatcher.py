import json
import utils
import scraper
import logging as log
import telegramclient as tc

updates_served = set()
waiting_reply = {}
users_locations = {}


def dispatch(updates):
    for update in [u for u in updates if u["update_id"] not in updates_served]:
        id = update["update_id"]
        log.info(update)
        process(update)
        updates_served.add(id)
        tc.set_offset(id)


def process(update):
    user_id = update["message"]["from"]["id"]
    user_name = update["message"]["from"]["username"]
    log.info("Received update %s from user %s" % (user_id, user_name))
    message = update["message"]
    if "reply_to_message" in message:
        if message["reply_to_message"]["message_id"] in waiting_reply:
            waiting_reply[message["reply_to_message"]["message_id"]](update)
        else:
            log.error("Not waiting for message %s" % message["message_id"])
    else:
        command_functions.get(message["text"], unknown_command)(update)


def handle_location_message(update):
    message = update["message"]
    user_id = update["message"]["from"]["id"]
    if "location" not in message:
        log.error("Could not find location in message %s" %
                  message["message_id"])
    else:
        location = message["location"]
        log.info("User located in lng: %f, lat: %f" %
                 (location["longitude"], location["latitude"]))
        users_locations[user_id] = location


def process_start(update):
    log.info("Processing start...")
    resp = tc.request_location_message(update["message"]["from"]["id"],
                                       "Ho bisogno della tua posizione " +
                                       "per sapere quali stazioni ti " +
                                       "sono piu' vicine",
                                       "Condividi la tua posizione")
    log.info("Setting waiting reply for message %d" % resp["message_id"])
    waiting_reply[resp["message_id"]] = handle_location_message


def process_nearest(update):
    user_id = update["message"]["from"]["id"]
    if user_id in users_locations:
        stations = scraper.scrape_bikes()
        nearest_station = utils.find_nearest(
            list(stations.values()),
            users_locations[user_id]["latitude"],
            users_locations[user_id]["longitude"]
        )
        tc.send_simple_message(user_id, str(nearest_station))
        tc.send_location(
            user_id,
            {
                'lat': nearest_station.lat,
                'lng': nearest_station.lng
            }
        )
    else:
        log.info(users_locations)
        process_start(update)


def unknown_command(update):
    log.error("Unable to process unknown update %s" % json.dumps(update))


command_functions = {
    '/start': process_start,
    '/nearest': process_nearest
}
