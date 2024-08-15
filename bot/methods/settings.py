import json
from django.views.decorators.csrf import csrf_exempt
from content.models import Grade, Class
from bot import strings
import persian
from .api import *
from user.models import User

def send_invite(user_id, chat_id):
    user = User.objects.get(user_id = user_id)

    send(
        'sendMessage',
        json.dumps({
            "chat_id": chat_id,
            "text": strings.invite_text2,
            "reply_markup": MENU,
        })
    )
    send(
        'sendPhoto',
        json.dumps({
            "chat_id": chat_id,
            "photo": "1274620264:-8761291616849682688:0:e61885f6087179c8d7c2f54fcdd42a151a9ec6f7595b78a8",
            "caption": strings.invite_text.format(str(user), user_id),
            "reply_markup": MENU,
        })
    )

def add_invite(user_id, invitee_id):
    user = User.objects.get(user_id = user_id)

    try:
        _ = int(invitee_id)
        valid = 1
    except: 
        valid = 0

    print(valid and User.objects.filter(user_id = invitee_id).exists())
    if valid and User.objects.filter(user_id = invitee_id).exists():
        inviter = User.objects.get(user_id=invitee_id)
        user.inviter = inviter
        user.save()

        inviter.calculated_score += 1001
        inviter.save()

def show_score(message, chat_id, user_id):
    user = User.objects.get(user_id=user_id)
    score = user.calculated_score

    counter = 1
    for i in User.objects.all():
        if (i.calculated_score > score):
            counter += 1

    send(
        'sendPhoto',
        json.dumps({
            "chat_id": chat_id,
            "from_chat_id": "@darsyarchannel",
            "photo": "1274620264:-7778577532524028157:0:01eb81afd8161218738d56623aa1fedb",
            "caption": strings.score.format(persian.convert_en_numbers(score), persian.convert_en_numbers(counter)),
            "reply_markup": MENU
        })
    )


def ask_role(message, user_id):
    user = User.objects.get(user_id=user_id)
    user.is_student = message['callback_query']['data'][1:] == '1'
    user.save()

    send(
        'sendMessage',
        json.dumps({
            "chat_id": message['callback_query']['message']['chat']['id'],
            "text": strings.new_grade,
            "reply_markup": {
                "inline_keyboard": [
                    [{"text": grade.name, "callback_data": "1"+str(grade.id)}] for grade in Grade.objects.order_by("grade_number")
                ]
            }
        })
    )


def choose_class(message, type, chat_id, user_id):
    user = User.objects.get(user_id=user_id)

    send(
        'sendMessage',
        json.dumps({
            "chat_id": chat_id,
            "text": strings.choose_class,
            "reply_markup": {
                "inline_keyboard": [
                    [{"text": cls.name, "callback_data": chr(ord('a') + type) + str(cls.id)}] for cls in user.grade.classes.all()
                ]
            }
        })
    )


def choose_unit(message, type):
    cls = Class.objects.all().get(
        id=int(message['callback_query']['data'][1:]))
    counter = 0
    for unit in cls.units.all():
        counter += unit.questions.count()

    send(
        'editMessageText',
        json.dumps({
            "chat_id": message['callback_query']['message']['chat']['id'],
            "message_id": message['callback_query']['message']['message_id'],
            "text": strings.choose_unit.format(cls, persian.convert_en_numbers(counter)),
            "reply_markup": {
                "inline_keyboard": [
                    [{"text": unit.name, "callback_data": chr(ord('c') + type) + str(unit.id)}] for unit in cls.units.all()
                ]
            }
        })
    )


def update_grade(message, user_id):
    user = User.objects.get(user_id=user_id)
    user.grade = Grade.objects.get(
        id=int(message['callback_query']['data'][1:]))
    user.save()

    send(
        'editMessageText',
        json.dumps({
            "chat_id": message['callback_query']['message']['chat']['id'],
            "message_id": message['callback_query']['message']['message_id'],
            "text": strings.confirm_grade.format(user.grade.name),
            "reply_markup": MENU
        })
    )

    send(
        'sendPhoto',
        json.dumps({
            "chat_id": message['callback_query']['message']['chat']['id'],
            "from_chat_id": "@darsyarchannel",
            "photo": "1274620264:-5975879736299086078:0:d2e8769499c774da902f88d87def11e2738d56623aa1fedb",
            "caption": strings.guide,
            "reply_markup": MENU,
        })
    )


def new_grade(chat_id):
    send(
        'sendMessage',
        json.dumps({
            "chat_id": chat_id,
            "text": strings.new_grade,
            "reply_markup": {
                "inline_keyboard": [
                    [{"text": grade.name, "callback_data": "1"+str(grade.id)}] for grade in Grade.objects.order_by("grade_number")
                ]
            }
        })
    )
