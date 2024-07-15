import json
import requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from bot.credintials import TOKEN, API_URL, URL
from user.models import User
from content.models import Grade
from bot import strings

MENU = {
        "keyboard": [
        [
          {
            "text": "⁉️ سوال جدید"
          },
          {
            "text": "Blue"
          },
          {
            "text": "Green"
          }
        ]]
      }

@csrf_exempt
def bot(request):
  if request.method == 'POST':
    message = json.loads(request.body.decode('utf-8'))
    #print(json.dumps(message, indent=2))
    
    if message.get('callback_query'):
        update_grade(message)
        return HttpResponse('ok')
    
    if message['message']['text'] == '/start':
      start(message)
      return HttpResponse('ok')
    
    
  return HttpResponse('ok')

def update_grade(message): 
  user = User.objects.get(user_id=message['callback_query']['from']['id'])
  user.grade = Grade.objects.get(id=int(message['callback_query']['data']))
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
          [{"text": grade.name, "callback_data": str(grade.id)} for grade in Grade.objects.all()]
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
          [{"text": grade.name, "callback_data": str(grade.id)} for grade in Grade.objects.all()]
        ]
      }
    })
  )

def menu(chat_id):
  send(
    'sendMessage',
    json.dumps({
      "chat_id": chat_id,
      "text": strings.menu,
      "reply_markup": {
      "keyboard": [
        [
          {
            "text": "Red"
          },
          {
            "text": "Blue"
          },
          {
            "text": "Green"
          }
        ]
      ]
    }
    })
  )
def bale_setwebhook(request):
  response = requests.post(API_URL+ "setWebhook?url=" + URL).json()
  return HttpResponse(f"{response}")

def send(method, data):
  return requests.post(API_URL + method, data)
