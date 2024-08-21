import json
from bot import strings
from bot.credintials import DARSYAR_GUIDE_FILE_ID, DARSYAR_IMAGE_FILE_ID, PLATFORM
from user.models import User
from .api import *
from content.models import Grade, Class, Unit, Question


def join_channel(chat_id):
    send(
        'sendMessage',
        {
            "chat_id": chat_id,
            "text": strings.join_channel,
            "reply_markup": json.dumps({
                "inline_keyboard": [
                    [{"text": strings.check_if_joined, "callback_data": "-"}],
                ]
            })
        }
    )


def help(chat_id):
    send(
        'sendPhoto',
        {
            "chat_id": chat_id,
            "from_chat_id": "@darsyarchannel",
            "photo": DARSYAR_GUIDE_FILE_ID,
            "caption": strings.guide,
            "reply_markup": MENU,
        }
    )

    send(
        'sendMessage',
        {
            "chat_id": chat_id,
            "text": strings.help,
            "reply_markup": MENU,
        }
    )


def channel(chat_id):
    send(
        'sendPhoto',
        {
            "chat_id": chat_id,
            "from_chat_id": "@darsyarchannel",
            "photo": DARSYAR_IMAGE_FILE_ID,
            "caption": strings.channel,
            "reply_markup": MENU
        }
    )


def support(chat_id):
    send(
        'sendPhoto',
        {
            "chat_id": chat_id,
            "from_chat_id": "@darsyarchannel",
            "photo": DARSYAR_IMAGE_FILE_ID,
            "caption": strings.support,
            "reply_markup": MENU
        }
    )


def start(chat_id, user_id):
    user = User.objects.get( platform = PLATFORM, user_id=user_id)

    send(
        'sendPhoto',
        {
            "chat_id": chat_id,
            "from_chat_id": "@darsyarchannel",
            "photo": DARSYAR_IMAGE_FILE_ID,
            "caption": strings.start.format(user),
            "reply_markup": json.dumps({
                "inline_keyboard": [
                    [{"text": strings.student, "callback_data": "01"}],
                    [{"text": strings.teacher, "callback_data": "00"}]
                ]
            })
        }
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
        {
            "chat_id": chat_id,
            "text": strings.unknown,
            "reply_markup": MENU,
        }
    )
