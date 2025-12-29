import json
from django.views.decorators.csrf import csrf_exempt
from bot.credintials import DARSYAR_GUIDE_FILE_ID, DARSYAR_IMAGE_FILE_ID, DARSYAR_SCORE_FILE_ID, PLATFORM
from content.models import Grade, Class
from bot import strings
import persian
from .api import *
from user.models import User
from bot.methods.general import help

def send_invite(user_id, chat_id):
    user = User.objects.get(platform=PLATFORM, user_id=user_id)

    send(
        'sendMessage',
        {
            "chat_id": chat_id,
            "text": strings.invite_text2,
            "reply_markup": MENU,
        }
    )
    send(
        'sendPhoto',
        {
            "chat_id": chat_id,
            "photo": DARSYAR_IMAGE_FILE_ID,
            "caption": strings.invite_text.format(str(user), user_id),
            "reply_markup": MENU,
        }
    )


def add_invite(user_id, invitee_id):
    user = User.objects.get(platform=PLATFORM, user_id=user_id)

    try:
        _ = int(invitee_id)
        valid = 1
    except:
        valid = 0

    # print(valid and User.objects.filter(user_id = invitee_id).exists())
    if valid and User.objects.filter(user_id=invitee_id).exists():
        inviter = User.objects.get(platform=PLATFORM, user_id=invitee_id)
        user.inviter = inviter
        user.save()

        inviter.calculated_score += 1001
        inviter.save()


def show_score(message, chat_id, user_id):
    user = User.objects.get(platform=PLATFORM, user_id=user_id)
    score = user.calculated_score

    counter = 1
    for i in User.objects.all():
        if (i.calculated_score > score):
            counter += 1

    send(
        'sendPhoto',
        {
            "chat_id": chat_id,
            "from_chat_id": "@darsyarchannel",
            "photo": DARSYAR_SCORE_FILE_ID,
            "caption": strings.score.format(persian.convert_en_numbers(score), persian.convert_en_numbers(counter)),
            "reply_markup": MENU
        }
    )


def ask_role(message, user_id):
    user = User.objects.get(platform=PLATFORM, user_id=user_id)
    user.is_student = message['callback_query']['data'][1:] == '1'
    user.save()

    send(
        'sendMessage',
        {
            "chat_id": message['callback_query']['message']['chat']['id'],
            "text": strings.new_grade,
            "reply_markup": json.dumps({
                "inline_keyboard": [
                    [{"text": grade.name, "callback_data": "1"+str(grade.id)}] for grade in Grade.objects.order_by("grade_number")
                ]
            })
        }
    )


def choose_class(message, type, chat_id, user_id):
    print("Choose Class")
    user = User.objects.get(platform=PLATFORM, user_id=user_id)

    classes = []
    for i in user.grade.classes.all():
        if i.has_questions():
            classes.append(i)

    print(json.dumps(send(
        'sendMessage',
        {
            "chat_id": chat_id,
            "text": strings.choose_class,
            "reply_markup": json.dumps({
                "inline_keyboard": [
                    [{"text": cls.name, "callback_data": chr(ord('a') + type) + str(cls.id)}] for cls in classes
                ]
            })
        }
    ), indent=4))

def reset_state(chat_id, user_id):
    user = User.objects.get(platform=PLATFORM, user_id=user_id)
    user.state = 0
    user.save()

    help(chat_id)

def choose_unit(message, type):
    print("Choose Unit")
    cls = Class.objects.all().get(
        id=int(message['callback_query']['data'][1:]))
    
    counter = 0
    for unit in cls.units.all():
        counter += unit.questions.count()

    units = []
    for i in cls.units.all():
        if i.questions.count() > 0:
            units.append(i)

    print(json.dumps(send(
        'editMessageText',
        {
            "chat_id": message['callback_query']['message']['chat']['id'],
            "message_id": message['callback_query']['message']['message_id'],
            "text": strings.choose_unit.format(cls, persian.convert_en_numbers(counter)),
            "reply_markup": json.dumps({
                "inline_keyboard": [
                    [{"text": unit.name, "callback_data": chr(ord('c') + type) + str(unit.id)}] for unit in units
                ]
            })
        }
    ), indent=4))


def update_grade(message, user_id):
    user = User.objects.get(platform=PLATFORM, user_id=user_id)
    user.grade = Grade.objects.get(
        id=int(message['callback_query']['data'][1:]))
    user.save()

    send(
        'editMessageText',
        {
            "chat_id": message['callback_query']['message']['chat']['id'],
            "message_id": message['callback_query']['message']['message_id'],
            "text": strings.confirm_grade.format(user.grade.name),
            "reply_markup": MENU
        }
    )

    send(
        'sendPhoto',
        {
            "chat_id": message['callback_query']['message']['chat']['id'],
            "from_chat_id": "@darsyarchannel",
            "photo": DARSYAR_GUIDE_FILE_ID,
            "caption": strings.guide,
            "reply_markup": MENU,
        }
    )


def new_grade(chat_id):
    send(
        'sendMessage',
        {
            "chat_id": chat_id,
            "text": strings.new_grade,
            "reply_markup": json.dumps({
                "inline_keyboard": [
                    [{"text": grade.name, "callback_data": "1"+str(grade.id)}] for grade in Grade.objects.order_by("grade_number")
                ]
            })
        }
    )
