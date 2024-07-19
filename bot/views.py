import json
import requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from bot.credintials import TOKEN, API_URL, URL
from user.models import User
from content.models import Grade, Class, Unit, Question
from bot import strings
from random import randint
import random
import persian
from bot.AI import ai

MENU = {
        "keyboard": [
        [
          {
            "text": strings.MenuStrings.new_question
          },
        ],
        [
          {
            "text": strings.MenuStrings.new_test
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
    print(json.dumps(message, indent=2))
    
    state = 0
    if message.get('message'):
      if message['message']['text'] != 'text' and (not User.objects.filter(user_id=message['message']['from']['id']).exists()):
        start(message)
      else:
          user = User.objects.get(user_id=int(message['message']['from']['id']))
          state = user.state > 0
    
    
    if state:
      check_answer(message)
          
    
    elif message.get('callback_query') and message['callback_query']['data'][0] == "1":
        update_grade(message)
    elif message.get('callback_query') and message['callback_query']['data'][0] == "a":
        choose_unit(message, 0)
    elif message.get('callback_query') and message['callback_query']['data'][0] == "b":
        choose_unit(message, 1)
    elif message.get('callback_query') and message['callback_query']['data'][0] == "c":
        new_question(message)
    elif message.get('callback_query') and message['callback_query']['data'][0] == "d":
        new_test(message)
    elif message.get('callback_query') and message['callback_query']['data'][0] == "4":
        show_answer(message)
    elif message.get('callback_query') and message['callback_query']['data'][0] == "5":
        switch_state(message)
    elif message.get('callback_query') and message['callback_query']['data'][0] == "6":
        help(message['callback_query']['message']['chat']['id'])
    
    elif message['message']['text'] == '/start':
        start(message)
    elif message['message']['text'] == strings.MenuStrings.new_question:
        choose_class(message, 0)
    elif message['message']['text'] == strings.MenuStrings.new_test:
       choose_class(message, 1)
    elif message['message']['text'] == strings.MenuStrings.change_grade:
        new_grade(message)
    elif message['message']['text'] == strings.MenuStrings.channel:
        channel(message)
    elif message['message']['text'] == strings.MenuStrings.support:
        support(message)
    else:
        Sticker(message)
    
    
  return HttpResponse('ok')

def help(chat_id):
   message_id = send(
    'sendMessage',
    json.dumps({
      "chat_id": chat_id,
      "text": strings.help,
      "reply_markup": MENU,
    })
  )
  
def check_answer(message):
  user = User.objects.get(user_id=int(message['message']['from']['id']))
  question = Question.objects.get(id=user.state)
  
  message_id = send(
    'sendMessage',
    json.dumps({
      "chat_id": message['message']['chat']['id'],
      "text": strings.wait,
    })
  )

  req = ai(question.text, question.answer, message['message']['text'])

  send(
    'editMessageText',
    json.dumps({
      "chat_id": message['message']['chat']['id'],
      "message_id": message_id,
      "text": strings.ai_answer.format(persian.convert_en_numbers(req['grade']), req['feedback'], question.answer),
      "reply_markup": MENU
    })
  )

  user.state = 0
  user.save()

def switch_state(message):
  print(message['callback_query']['from']['id'])
  user = User.objects.get(user_id=int(message['callback_query']['from']['id']))
  user.state = int(message['callback_query']['data'][1:])
  user.save()

  send(
    'sendMessage',
    json.dumps({
      "chat_id": message['callback_query']['message']['chat']['id'],
      "text": strings.send_answer,
    })
  )

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

def show_answer(message):
  q = Question.objects.get(id=int(message['callback_query']['data'][1:]))

  send(
    'sendMessage',
    json.dumps({
      "chat_id": message['callback_query']['message']['chat']['id'],
      "text": q.answer, 
      "reply_markup": MENU
    })
  )

def new_test(message):
  print(message['callback_query']['data'])
  unit = Unit.objects.all().get(id = int(message['callback_query']['data'][1:]))
  q = randint(0, unit.questions.count()-1)
  test = random.sample(list(unit.questions.all()), 5)


  text = ""
  for i in test:
    text += i.text
    text += "\n"

  send(
    'sendMessage',
    json.dumps({
      "chat_id": message['callback_query']['message']['chat']['id'],
      "text": text,
      "reply_markup": MENU
    })
  )

def new_question(message):
  print(message['callback_query']['data'])
  unit = Unit.objects.all().get(id = int(message['callback_query']['data'][1:]))
  q = randint(0, unit.questions.count()-1)

  send(
    'sendMessage',
    json.dumps({
      "chat_id": message['callback_query']['message']['chat']['id'],
      #"message_id": message['callback_query']['message']['message_id'],
      "text": strings.question.format(unit, unit.questions.all()[q].text),
      "reply_markup": {
        "inline_keyboard": [
          [{
            "text": strings.show_answer,
            "callback_data": "4" + str(unit.questions.all()[q].id),
          }],
          [{
            "text": strings.check_answer,
            "callback_data": "5" + str(unit.questions.all()[q].id),
          }],
          [{
             "text": strings.next_question,
            "callback_data": "3" + str(unit.id),
          }],
          [{
             "text": strings.show_help,
             "callback_data": "6",
          }]
        ]
      }
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
  send(
    'editMessageText',
    json.dumps({
      "chat_id": message['callback_query']['message']['chat']['id'],
      "message_id": message['callback_query']['message']['message_id'],
      "text": strings.choose_unit.format(cls),
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
          [{"text": grade.name, "callback_data": "1"+str(grade.id)}] for grade in Grade.objects.all()
        ]
      }
    })
  )

def start(message):
  if (not User.objects.filter(user_id=message['message']['from']['id']).exists()):
    user = User.objects.create(user_id=message['message']['from']['id'], first_name= message['message']['from']['first_name'], last_name=message['message']['from']['last_name'])
  else: 
    user = User.objects.get(user_id=message['message']['from']['id'])
  
  send(
    'sendMessage',
    json.dumps({
      "chat_id": message['message']['chat']['id'],
      "text": strings.start.format(user),
      "reply_markup": {
        "inline_keyboard": [
          [{"text": grade.name, "callback_data": "1"+str(grade.id)}] for grade in Grade.objects.all()
        ]
      }
    })
  )

def bale_setwebhook(request):
  response = requests.post(API_URL+ "setWebhook?url=" + request.build_absolute_uri('/')).json()
  return HttpResponse(f"{response}")

def send(method, data):
  return requests.post(API_URL + method, data).json()['result']['message_id']

def Sticker(message):
  print(message['message']['from']['id'])
  try:
     send(
      'sendAnimation',
      {
          "chat_id": message['message']['from']['id'],
          "animation": "1409599563:-356479065845784830:1:1a9ec6f7595b78a8"
      }
    )
  except:
     send(
      'sendAnimation',
      {
          "chat_id": message['callback_query']['message']['from']['id'],
          "animation": "1409599563:-356479065845784830:1:1a9ec6f7595b78a8"
      }
    )