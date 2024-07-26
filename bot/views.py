import json
import os
import requests
from django.http import FileResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from bot.credintials import TOKEN, API_URL, URL
from user.models import User, UserQuestionRel
from content.models import Grade, Class, Unit, Question, Source
from django.template import loader
from bot import strings
import pdfkit
import tempfile
from random import randint
import random
import persian
from bot.AI import ai
from django.shortcuts import render
from .methods.general import *
from .methods.test import *
from .methods.question import *
from .methods.settings import *
from .scraper import scrape

def scraper(request):
    #grade = Grade.objects.filter(id = request.GET.get('grade'))
    
    cls = Class.objects.create(name = request.GET.get('class'), grade_number = request.GET.get('grade_number'))
    #cls.grades.add(grade)
    source = Source.objects.get(id = 1)
    number = scrape(cls, source, request.GET.get('link'))
    return HttpResponse(f"{number} questions scraped succesfully!")
   
@csrf_exempt
def bot(request):
  if request.method == 'POST':
    message = json.loads(request.body.decode('utf-8'))
    #print(json.dumps(message, indent=2))
    
    state = 0
    if message.get('message'):
      if message['message']['text'] != 'text' and (not User.objects.filter(user_id=message['message']['from']['id']).exists()):
        start(message)
      else:
          user = User.objects.get(user_id=int(message['message']['from']['id']))
          state = user.state > 0
    
    
    if state:
      check_answer(message)
          
    
    elif message.get('callback_query') and message['callback_query']['data'][0] == "1":
        update_grade(message)
    elif message.get('callback_query') and message['callback_query']['data'][0] == "a":
        choose_unit(message, 0)
    elif message.get('callback_query') and message['callback_query']['data'][0] == "b":
        choose_unit(message, 1)
    elif message.get('callback_query') and message['callback_query']['data'][0] == "c":
        new_question(message)
    elif message.get('callback_query') and message['callback_query']['data'][0] == "d":
        new_test(message, request.build_absolute_uri('/'))
    elif message.get('callback_query') and message['callback_query']['data'][0] == "4":
        show_answer(message)
    elif message.get('callback_query') and message['callback_query']['data'][0] == "5":
        switch_state(message)
    elif message.get('callback_query') and message['callback_query']['data'][0] == "6":
        help(message['callback_query']['message']['chat']['id'])
    
    elif message['message']['text'] == '/start':
        start(message)
    elif message['message']['text'] == strings.MenuStrings.new_question:
        choose_class(message, 0)
    elif message['message']['text'] == strings.MenuStrings.new_test:
       choose_class(message, 1)
    elif message['message']['text'] == strings.MenuStrings.show_score:
        show_score(message)
    elif message['message']['text'] == strings.MenuStrings.change_grade:
        new_grade(message)
    elif message['message']['text'] == strings.MenuStrings.channel:
        channel(message)
    elif message['message']['text'] == strings.MenuStrings.support:
        support(message)
    else:
        Sticker(message)
    
    
  return HttpResponse('ok')

def bale_setwebhook(request):
  response = requests.post(API_URL+ "setWebhook?url=" + request.build_absolute_uri('/')).json()
  return HttpResponse(f"{response}")

