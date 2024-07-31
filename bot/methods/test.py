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
from .api import *

def get_html(request, unitid):
  unit = Unit.objects.all().get(id = int(unitid))
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
  return render(request, 'exam.html', {"questions": random_questions_objects, "unit": unit.name, "date": JalaliDateTime.now(pytz.utc).strftime("%Y/%m/%d")})
  

def new_test(message, url):
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
  print(fileurl)
  send(
    'sendDocument',
    json.dumps({
      "chat_id": message['callback_query']['message']['chat']['id'],
      "document": fileurl,
      "reply_markup": MENU,
      "caption": strings.test_caption.format(unit.class_rel.grades[0].name, unit.class_rel.name, unit.name),
    })
  )
