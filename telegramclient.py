import logging as log
import urllib.request
import urllib.parse
import json
import os

TOKEN = os.getenv('BOT_TOKEN')

if not TOKEN:
    raise Exception("Token not set, Set it in the OS Environment")

BASE_URL = 'https://api.telegram.org/bot%s/' % TOKEN


def get_updates():
    req = urllib.request.Request(
        BASE_URL + 'getUpdates',
        data=None
    )
    with urllib.request.urlopen(req) as resp:
        updates = json.loads(resp.read())
        if updates["ok"]:
            return updates["result"]
        else:
            raise Exception(
                "Error while getting updates: (%d) %s" %
                (updates["error_code"], updates["description"])
            )


def send_message(user_id, message):
    body = {
        'chat_id': user_id,
        'text': message
    }
    req = urllib.request.Request(
        BASE_URL + 'sendMessage',
        data=urllib.parse.urlencode(body).encode()
    )
    with urllib.request.urlopen(req) as resp:
        jsonResponse = json.loads(resp.read())
        log.info(jsonResponse)
