import json
from django.http import FileResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from weasyprint import HTML
from content.models import Unit
from django.shortcuts import render
from django.template import loader
from persiantools.jdatetime import JalaliDateTime
from asgiref.sync import async_to_sync
import pytz
import tempfile
from random import randint
import random
from .logs import log_requests
from user.models import User
from .api import *

def get_html(request, unit_id):
  unit = Unit.objects.all().get(id = int(unit_id))
  questions = list(unit.questions.all())
  random_questions = random.sample(questions, 5)
  random_questions_objects = [
    {
        'text': question.text,
        'answer': question.answer, 
        'sourceText': question.source.name if question.source else None
    }
    for question in random_questions
  ]
  return render(request, 'exam.html', {"questions": random_questions_objects, "unit": unit.class_rel.name, "date": JalaliDateTime.now(pytz.utc).strftime("%Y/%m/%d")})
  

def new_test(message, url):
  
  message_id = send(
    'editMessageText',
    json.dumps({
      "chat_id": message['callback_query']['message']['chat']['id'],
      "message_id": message['callback_query']['message']['message_id'],
      "text": strings.wait,
    })
  )
  #print(message['callback_query']['data'])
  unit = Unit.objects.all().get(id = int(message['callback_query']['data'][1:]))
  file = tempfile.NamedTemporaryFile(delete=True, suffix=".pdf")
  HTML(url=f'{url}gethtml/{unit.id}').write_pdf(file.name)
  upload_url = "https://tmpfiles.org/api/v1/upload"
  files=[
    ('file',('exam.pdf',open(file.name,'rb')))
  ]
  response = requests.post(upload_url, files=files)
  fileurl = response.json()['data']['url'].replace("https://tmpfiles.org/", "https://tmpfiles.org/dl/")
  user = User.objects.get(user_id=message['callback_query']['from']['id'])
  send(
    'sendDocument',
    json.dumps({
      "chat_id": message['callback_query']['message']['chat']['id'],
      "document": fileurl,
      "reply_markup": MENU,
      "caption": strings.test_caption.format(user.grade.name, unit.class_rel.name, unit.name),
    })
  )
  
  send(
    'deleteMessage',
    json.dumps({
      "chat_id": message['callback_query']['message']['chat']['id'],
      "message_id": message['callback_query']['message']['message_id'],
    })
  )

  log_requests(user, unit, 0, 1)
