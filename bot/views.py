import json
import requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .credintials import TOKEN, API_URL, URL
from user.models import User
from bot import strings
@csrf_exempt
def bot(request):
  if request.method == 'POST':
    message = json.loads(request.body.decode('utf-8'))

    if message['message']['text'] == '/start':
      start(message)
      return HttpResponse('ok')
    
    
  return HttpResponse('ok')

def start(message):
  if (not User.objects.filter(user_id=message['message']['from']['id']).exists()):
    user = User.objects.create(user_id=message['message']['from']['id'])
  send(
    'sendMessage',
    json.dumps({
  "chat_id": 2130762647,
  "text": "salalamamamamam",
  "reply_markup": {
    "inline_keyboard": [
      [
        {
          "text": "Red",
          "callback_data": "Red"
        },
        {
          "text": "Blue",
          "callback_data": "Blue"
        },
        {
          "text": "Green",
          "callback_data": "Green"
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
