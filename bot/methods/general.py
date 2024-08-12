import json
from bot import strings
from user.models import User
from .api import *
from content.models import Grade, Class, Unit, Question

def help(chat_id):
   send(
     'sendPhoto',
     json.dumps({
      "chat_id": chat_id,
      "from_chat_id": "@darsyarchannel",
      "photo": "1274620264:-5975879736299086078:0:d2e8769499c774da902f88d87def11e2738d56623aa1fedb",
      "caption": strings.guide,
      "reply_markup": MENU,
    })
   )
   send(
    'sendMessage',
    json.dumps({
      "chat_id": chat_id,
      "text": strings.help,
      "reply_markup": MENU,
    })
  )

def channel(message): 
  send(
    'sendPhoto',
    json.dumps({
      "chat_id": message['message']['chat']['id'],
      "from_chat_id": "@darsyarchannel",
      "photo": "1274620264:-8761291616849682688:0:e61885f6087179c8d7c2f54fcdd42a151a9ec6f7595b78a8",
      "caption": strings.channel,
      "reply_markup": MENU
    })
  )

def support(message):
  send(
    'sendPhoto',
    json.dumps({
      "chat_id": message['message']['chat']['id'],
      "from_chat_id": "@darsyarchannel",
      "photo": "1274620264:-8761291616849682688:0:e61885f6087179c8d7c2f54fcdd42a151a9ec6f7595b78a8",
      "caption": strings.support,
      "reply_markup": MENU
    })
  )

def start(message):
  if (not User.objects.filter(user_id=message['message']['from']['id']).exists()):
    user = User.objects.create(user_id=message['message']['from']['id'], first_name= message['message']['from']['first_name'], last_name=message['message']['from']['last_name'])
  else: 
    user = User.objects.get(user_id=message['message']['from']['id'])
  
  send(
    'sendPhoto',
    json.dumps({
      "chat_id": message['message']['chat']['id'],
      "from_chat_id": "@darsyarchannel",
      "photo": "1274620264:-8761291616849682688:0:e61885f6087179c8d7c2f54fcdd42a151a9ec6f7595b78a8",
      "caption": strings.start.format(user),
      "reply_markup": {
        "inline_keyboard": [
          [{"text": strings.student, "callback_data": "01"}],
          [{"text": strings.teacher, "callback_data": "00"}]
        ]
      }
    })
  )

def Sticker(message):
  try:
     send(
      'sendAnimation',
      {
          "chat_id": message['message']['from']['id'],
          "animation": "1409599563:-356479065845784830:1:1a9ec6f7595b78a8",
          "reply_markup": MENU
      }
    )
     send(
        'sendMessage',
        json.dumps({
          "chat_id": message['message']['from']['id'],
          "text": strings.unknown,
          "reply_markup": MENU,
        })
      )
    
  except:
     send(
      'sendAnimation',
      {
          "chat_id": message['callback_query']['message']['from']['id'],
          "animation": "1409599563:-356479065845784830:1:1a9ec6f7595b78a8",
          "reply_markup": MENU
      }
    )
     send(
        'sendMessage',
        json.dumps({
          "chat_id": message['callback_query']['message']['from']['id'],
          "text": strings.unknown,
          "reply_markup": MENU,
        })
      )
