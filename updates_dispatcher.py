import logging as log
import telegramclient


updates_served = set()


def dispatch(updates):
    log.info(updates)
    for update in [u for u in updates if u["update_id"] not in updates_served]:
        id = update["update_id"]
        process(update)
        updates_served.add(id)


def process(update):
    user_id = update["message"]["from"]["id"]
    user_name = update["message"]["from"]["username"]
    log.info("Received update %s from user %s" % (user_id, user_name))
    command_functions.get(update["message"]["text"], unknown_command)(update)


def process_start(update):
    log.info("Processing start...")
    telegramclient.send_message(update["message"]["from"]["id"], "Ciao")


def unknown_command(update):
    log.error("Command %s is unknown, skipping..." % update["text"])


command_functions = {
    '/start': process_start
}
