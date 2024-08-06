import json
from django.views.decorators.csrf import csrf_exempt
from content.models import Grade, Class, Unit
from bot import strings
import persian
from .api import *
from user.models import User


def log_requests(message):
    print("log")
    format = "#question" if message['callback_query']['data'][0] == 'c' else "#test"
    user = User.objects.get(user_id=int(message['callback_query']['from']['id']))
    unit = Unit.objects.all().get(id = int(message['callback_query']['data'][1:]))

    send(
        'sendMessage',
        json.dumps({
            "chat_id": "5868778639",
            "text": strings.log.format(format, user, user.user_id, user.grade, unit.class_rel, unit.name),
        })
    )