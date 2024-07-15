import json
import requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from bot.credintials import TOKEN, API_URL, URL
from user.models import User
from content.models import Grade, Class, Question
from bot import strings
from random import randint

MENU = {
        "keyboard": [
        [
          {
            "text": strings.MenuStrings.new_question
          },
        ],
        [
          {
            "text": strings.MenuStrings.change_grade
          },
        ],
        [
          {
            "text": strings.MenuStrings.channel
          },
          {
            "text": strings.MenuStrings.support
          }
        ]]
      }

@csrf_exempt
def bot(request):
  if request.method == 'POST':
    message = json.loads(request.body.decode('utf-8'))
    #print(json.dumps(message, indent=2))
    
    if message.get('callback_query') and message['callback_query']['data'][0] == "1":
        update_grade(message)
    elif message.get('callback_query') and message['callback_query']['data'][0] == "2":
        new_question(message)
    
    elif message['message']['text'] == '/start':
      start(message)
    elif message['message']['text'] == strings.MenuStrings.new_question:
      choose_class(message)
    elif message['message']['text'] == strings.MenuStrings.change_grade:
      new_grade(message)
    elif message['message']['text'] == strings.MenuStrings.channel:
      channel(message)
    elif message['message']['text'] == strings.MenuStrings.support:
      support(message)
    
  return HttpResponse('ok')

def channel(message): 
  send(
    'sendMessage',
    json.dumps({
      "chat_id": message['message']['chat']['id'],
      "text": strings.channel,
      "reply_markup": MENU
    })
  )

def support(message):
  send(
    'sendMessage',
    json.dumps({
      "chat_id": message['message']['chat']['id'],
      "text": strings.support,
      "reply_markup": MENU
    })
  )

def new_question(message):
  print(message['callback_query']['data'])
  cls = Class.objects.all().get(id = int(message['callback_query']['data'][1:]))
  q = randint(0, cls.questions.count()-1)

  send(
    'sendMessage',
    json.dumps({
      "chat_id": message['callback_query']['message']['chat']['id'],
      "text": cls.questions.all()[q].text,
    })
  )

def choose_class(message):
  user = User.objects.get(user_id = message['message']['from']['id'])
  send(
    'sendMessage',
    json.dumps({
      "chat_id": message['message']['chat']['id'],
      "text": strings.new_question,
      "reply_markup": {
        "inline_keyboard": [
          [{"text": cls.name, "callback_data": "2" + str(cls.id)}] for cls in user.grade.classes.all()
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
          [{"text": grade.name, "callback_data": "1"+str(grade.id)}] for grade in Grade.objects.all()
        ]
      }
    })
  )

def start(message):
  if (not User.objects.filter(user_id=message['message']['from']['id']).exists()):
    user = User.objects.create(user_id=message['message']['from']['id'])

  send(
    'sendMessage',
    json.dumps({
      "chat_id": message['message']['chat']['id'],
      "text": strings.start,
      "reply_markup": {
        "inline_keyboard": [
          [{"text": grade.name, "callback_data": "1"+str(grade.id)}] for grade in Grade.objects.all()
        ]
      }
    })
  )

def bale_setwebhook(request):
  response = requests.post(API_URL+ "setWebhook?url=" + URL).json()
  return HttpResponse(f"{response}")

def send(method, data):
  return requests.post(API_URL + method, data)
