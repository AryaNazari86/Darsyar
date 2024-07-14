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

def help(message): 
    chat_id = message['message']['chat']['id']

    send(
      "sendMessage", {
        'chat_id': chat_id,
        'text' :"asdasd",
        'reply_markup': {
          'keyboard': [
            {
              'text': "test",

            },
          ]
        }
      }
    )
  
def info(message):
  chat_id = message['message']['chat']['id']
  sender = message['message']['from']
  ff = message['message'].get('forward_from')
  if ff:
      send("sendMessage", {
      'chat_id': chat_id,
      'text': f"{ff['id']} \n@{ff['username']}\nhttps://web.bale.ai/chat?uid={ff['id']}",
      'reply_to_message_id': message['message']['message_id'],
      })
  else:
    send("sendMessage", {
      'chat_id': chat_id,
      'text': f"{sender['id']} \n@{sender['username']}\nhttps://web.bale.ai/chat?uid={sender['id']}",
      'reply_to_message_id': message['message']['message_id'],
      })

def ip_address(message):
  chat_id = message['message']['chat']['id']
  ip = message['message']['text'][4:]
  print(ip)

  req = requests.get('http://ip-api.com/json/' + ip).json()
  print('http://ip-api.com/json/' + ip)
  if (req['status']) == 'fail' or not ('.' in ip):
    send("sendMessage", {
        'chat_id': chat_id,
        'text': f"آدرس آی پی وارد شده نامعتبر می‌باشد.",
        'reply_to_message_id': message['message']['message_id'],
        })
    return
  
  print(json.dumps(req, indent = 4))
  
  '''
  {
    "status": "success",
    "country": "Iran",
    "countryCode": "IR",
    "region": "23",
    "regionName": "Tehran",
    "city": "Eslamshahr",
    "zip": "",
    "lat": 35.5522,
    "lon": 51.235,
    "timezone": "Asia/Tehran",
    "isp": "Mobile Communication Company of Iran",
    "org": "Mobile Communication Company",
    "as": "AS197207 Mobile Communication Company of Iran PLC",
    "query": "5.208.47.125"
  }
  '''
  send("sendMessage", {
        'chat_id': chat_id,
        'text': f"کشور: {req['country']}\شهر: {req['city']}",
        'reply_to_message_id': message['message']['message_id'],
        })
  send("sendLocation", {
        'chat_id': chat_id,
        'latitude': req['lat'],
        'longitude': req['lon'],
        'reply_to_message_id': message['message']['message_id'],
        })

def start(message):
  send("sendMessage", {
        'chat_id': message['message']['chat']['id'],
        'text': "سلام! ✋\nاسم من اینفو هست 🤖. من می‌تونم بهت توی به دست آوردن اطلاعات باحال کمک بکنم\n\nگرفتن اطلاعات چت  💬\nاگر یک توصعه کننده هستی یا به هر دلیلی نیاز به اطلاعات بله‌ی فرستنده‌ی یک پیام هستی، پیام مد نظرت رو از هرجایی برای من بازارسال کن و این اطلاعات رو از من دریافت کن!\n\nگرفتن اطلاعات از آدرس آی پی 📍\nکامند /ip به دنبال یک فاصله و بعد آدرس آی پی مدنظرت رو بفرست تا من بهت بگم این آی پی متعلق به کجاست. حواست باشه که از این اطلاعات فقط برای توصعه و دولوپ استفاده کنی و نه چیز دیگه!\n",
        'reply_to_message_id': message['message']['message_id'],
        })

def bale_setwebhook(request):
  response = requests.post(API_URL+ "setWebhook?url=" + URL).json()
  return HttpResponse(f"{response}")

def send(method, data):
  return requests.post(API_URL + method, data)
