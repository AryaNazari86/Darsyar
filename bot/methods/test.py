import json
from django.http import FileResponse
from django.views.decorators.csrf import csrf_exempt
from content.models import Unit
from django.template import loader
from persiantools.jdatetime import JalaliDateTime
import pdfkit
import pytz
import tempfile
from random import randint
import random
from .api import *

def get_pdf(request):
  unit_id = request.GET.get("unitid")
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

  filename = tempfile.NamedTemporaryFile(delete=True, suffix=".pdf").name
  
  html_str = loader.render_to_string('exam.html', {"questions": random_questions_objects, "unit": unit.name, "date": JalaliDateTime.now(pytz.utc).strftime("%Y/%m/%d")})
  pdfkit.from_string(html_str, filename, options={
     "encoding": "UTF-8"
  })
  response = FileResponse(open(filename, 'rb'))
  return response
  


def new_test(message, url):
  print(message['callback_query']['data'])
  unit = Unit.objects.all().get(id = int(message['callback_query']['data'][1:]))
  q = randint(0, unit.questions.count()-1)
  test = random.sample(list(unit.questions.all()), 5)


  print(f"{url}getpdf?unitid={unit.id}")

  send(
    'sendDocument',
    json.dumps({
      "chat_id": message['callback_query']['message']['chat']['id'],
      "document": f"{url}getpdf?unitid={unit.id}",
      "reply_markup": MENU
    })
  )
