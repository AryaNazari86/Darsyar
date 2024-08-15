import json
from bot import strings
from user.models import User
from .api import *
from content.models import Grade, Class, Unit, Question


def join_channel(chat_id):
    send(
        'sendMessage',
        json.dumps({
            "chat_id": chat_id,
            "text": strings.join_channel,
            "reply_markup": {
                "inline_keyboard": [
                    [{"text": strings.check_if_joined, "callback_data": "-"}],
                ]
            }
        })
    )


def help(chat_id):
    send(
        'sendPhoto',
        json.dumps({
            "chat_id": chat_id,
            "from_chat_id": "@darsyarchannel",
            "photo": "1274620264:-5975879736299086078:0:d2e8769499c774da902f88d87def11e2738d56623aa1fedb",
            "caption": strings.guide,
            "reply_markup": MENU,
        })
    )

    send(
        'sendMessage',
        json.dumps({
            "chat_id": chat_id,
            "text": strings.help,
            "reply_markup": MENU,
        })
    )


def channel(chat_id):
    send(
        'sendPhoto',
        json.dumps({
            "chat_id": chat_id,
            "from_chat_id": "@darsyarchannel",
            "photo": "1274620264:-8761291616849682688:0:e61885f6087179c8d7c2f54fcdd42a151a9ec6f7595b78a8",
            "caption": strings.channel,
            "reply_markup": MENU
        })
    )


def support(chat_id):
    send(
        'sendPhoto',
        json.dumps({
            "chat_id": chat_id,
            "from_chat_id": "@darsyarchannel",
            "photo": "1274620264:-8761291616849682688:0:e61885f6087179c8d7c2f54fcdd42a151a9ec6f7595b78a8",
            "caption": strings.support,
            "reply_markup": MENU
        })
    )


def start(chat_id, user_id):
    user = User.objects.get(user_id=user_id)

    send(
        'sendPhoto',
        json.dumps({
            "chat_id": chat_id,
            "from_chat_id": "@darsyarchannel",
            "photo": "1274620264:-8761291616849682688:0:e61885f6087179c8d7c2f54fcdd42a151a9ec6f7595b78a8",
            "caption": strings.start.format(user),
            "reply_markup": {
                "inline_keyboard": [
                    [{"text": strings.student, "callback_data": "01"}],
                    [{"text": strings.teacher, "callback_data": "00"}]
                ]
            }
        })
    )


def Sticker(chat_id):
    send(
        'sendAnimation',
        {
            "chat_id": chat_id,
            "animation": "1409599563:-356479065845784830:1:1a9ec6f7595b78a8",
            "reply_markup": MENU
        }
    )
    send(
        'sendMessage',
        json.dumps({
            "chat_id": chat_id,
            "text": strings.unknown,
            "reply_markup": MENU,
        })
    )
