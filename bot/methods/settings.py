import json
from django.views.decorators.csrf import csrf_exempt
from content.models import Grade, Class
from bot import strings
import persian
from .api import *
from user.models import User

def show_score(message):
  user = User.objects.get(user_id=int(message['message']['from']['id']))
  
  send(
     'sendMessage',
     json.dumps({
        "chat_id": message['message']['chat']['id'],
        "text": strings.score.format(persian.convert_en_numbers(user.score())),
        "reply_markup": MENU
     })
  )


def choose_class(message, type):
  user = User.objects.get(user_id = message['message']['from']['id'])

  send(
    'sendMessage',
    json.dumps({
      "chat_id": message['message']['chat']['id'],
      "text": strings.choose_class,
      "reply_markup": {
        "inline_keyboard": [
          [{"text": cls.name, "callback_data": chr(ord('a') + type) + str(cls.id)}] for cls in user.grade.classes.all()
        ]
      }
    })
  )

def choose_unit(message, type):
  cls = Class.objects.all().get(id = int(message['callback_query']['data'][1:]))
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

def update_grade(message): 
  user = User.objects.get(user_id=message['callback_query']['from']['id'])
  user.grade = Grade.objects.get(id=int(message['callback_query']['data'][1:]))
  user.save()

  send(
    'sendMessage',
    json.dumps({
      "chat_id": message['callback_query']['message']['chat']['id'],
      "text": f"شما در {user.grade.name} هستید.",
      "reply_markup": MENU
    })
  )

def new_grade(message):
  send(
    'sendMessage',
    json.dumps({
      "chat_id": message['message']['chat']['id'],
      "text": strings.new_grade,
      "reply_markup": {
        "inline_keyboard": [
          [{"text": grade.name, "callback_data": "1"+str(grade.id)}] for grade in Grade.objects.order_by("grade_number")
        ]
      }
    })
  )
