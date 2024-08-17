import json
from django.views.decorators.csrf import csrf_exempt
from content.models import Grade, Class, Unit
from bot import strings
import persian
from .api import *
from user.models import User
from bot.models import LOG


def log_requests(user, unit, question=0, t=0):
    # print("log")
    # print(question, t)
    if t == 0:
        format = f"#Question {question}"
    elif t == 1:
        format = "#Test"
    elif t == 2:
        format = f"#AI {question}"
    elif t == 3:
        format = f"#Hint {question}"

    # format = f"#question {question}" if (message['callback_query']['data'][0] == 'c' or message['callback_query']['data'][0] == 'C') else "#test"
    # user = User.objects.get(user_id=int(message['callback_query']['from']['id']))
    # unit = Unit.objects.get(id = int(message['callback_query']['data'][1:]))

    send(
        'sendMessage',
        json.dumps({
            "chat_id": "5868778639",
            "text": strings.log.format(format, user, user.user_id, user.grade, unit.class_rel, unit.name, question),
        })
    )

    lg = LOG.objects.create(user=user, type=t)
    lg.save()
