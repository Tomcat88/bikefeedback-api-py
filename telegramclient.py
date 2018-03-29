from types import SimpleNamespace as Namespace
import urllib
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
        updates = json.loads(resp.read(), object_hook=lambda d: Namespace(**d))
        if updates.ok:
            return updates.result
        else:
            raise Exception(
                "Error while getting updates: (%d) %s" %
                updates.error_code, updates.description
            )
