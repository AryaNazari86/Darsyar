import json
import requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .credintials import TOKEN, API_URL, URL

@csrf_exempt
def telegram_bot(request):
  if request.method == 'POST':
    message = json.loads(request.body.decode('utf-8'))

    if message['message']['text'] == '/start':
      start(message)
      return HttpResponse('ok')
    
    if message['message']['text'][0:3] == '/ip':
      ip_address(message)
      return HttpResponse('ok')
    
    info(message)
    #help(message)
    
  return HttpResponse('ok')

def bale_setwebhook(request):
  response = requests.post(API_URL+ "setWebhook?url=" + URL).json()
  return HttpResponse(f"{response}")

def send(method, data):
  return requests.post(API_URL + method, data)
