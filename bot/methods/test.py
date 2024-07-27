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
  
def get_pdf(request, unitid):
  file = tempfile.NamedTemporaryFile(delete=True, suffix=".pdf")
  HTML(url=request.build_absolute_uri(f'/gethtml/{unitid}')).write_pdf(file.name)
  response = HttpResponse(file, content_type='application/pdf')
  response['Content-Disposition'] = 'attachment; filename="' + file.name + '"'
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
