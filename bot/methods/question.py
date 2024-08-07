import json
from user.models import User, UserQuestionRel
from content.models import Unit, Question
from bot import strings
from random import randint
import persian
from bot.AI import ai
from .api import *
from .logs import *

def check_answer(message):
  """send(
    'sendChatAction',
    json.dumps({
      "chat_id": message['message']['chat']['id'],
      "action": strings.making_pdf,
    })
  )"""

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

  if not UserQuestionRel.objects.filter(user = user, question = question).exists():
      rel = UserQuestionRel.objects.create(user=user, question=question, point = req['grade'])
      rel.save()
  
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
  #print(message['callback_query']['from']['id'])
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

def show_answer(message):
  q = Question.objects.get(id=int(message['callback_query']['data'][1:]))

  send(
    'editMessageText',
    json.dumps({
      "chat_id": message['callback_query']['message']['chat']['id'],
      "message_id": message['callback_query']['message']['message_id'],
      "text": strings.answer_text.format(q.text, q.answer), 
      "reply_markup": MENU
    })
  )

def new_question(message):
  unit = Unit.objects.all().get(id = int(message['callback_query']['data'][1:]))
  q = randint(0, unit.questions.count()-1)
  log_requests(message, unit.questions.all()[q])

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
            "callback_data": "c" + str(unit.id),
          }],
          [{
             "text": strings.show_help,
             "callback_data": "6",
          }]
        ]
      }
    })
  )
