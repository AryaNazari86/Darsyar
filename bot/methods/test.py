import json
from django.http import FileResponse
from django.views.decorators.csrf import csrf_exempt
from weasyprint import HTML
from content.models import Unit
from django.template import loader
from persiantools.jdatetime import JalaliDateTime
from asgiref.sync import async_to_sync
import pytz
import tempfile
from random import randint
import random
from .api import *

def get_pdf(request, unitid):
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

  filename = tempfile.NamedTemporaryFile(delete=True, suffix=".pdf").name
  html_str = loader.render_to_string('exam.html', {"questions": random_questions_objects, "unit": unit.name, "date": JalaliDateTime.now(pytz.utc).strftime("%Y/%m/%d")})
  
  HTML(string=html_str).write_pdf(filename)

  response = FileResponse(open(filename, 'rb'))
  return response
  


def new_test(message, url):
  #print(message['callback_query']['data'])
  unit = Unit.objects.all().get(id = int(message['callback_query']['data'][1:]))
  q = randint(0, unit.questions.count()-1)
  test = random.sample(list(unit.questions.all()), 5)


  
  
  url = url.replace('http', 'https')
  print(f"{url}getpdf/{unit.id}/exam.pdf")

  send(
    'sendDocument',
    json.dumps({
      "chat_id": message['callback_query']['message']['chat']['id'],
      "document": f"{url}getpdf/{unit.id}/exam.pdf",
      "reply_markup": MENU
    })
  )
