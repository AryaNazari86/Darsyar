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
from . import hamyar

def scraper(request):
    #grade = Grade.objects.filter(id = request.GET.get('grade'))
    
    if not Class.objects.filter(name = request.GET.get('class')).exists:
        cls = Class.objects.get(name = request.GET.get('class'))
    else:
        cls = Class.objects.create(name = request.GET.get('class'), grade_number = request.GET.get('grade_number'))
    #cls.grades.add(grade)
    source = Source.objects.get(id = 1)
    number = scrape(cls, source, request.GET.get('link'))
    return HttpResponse(f"{number} questions scraped succesfully!")

def scrape_hamyar(request):
    #grade = Grade.objects.filter(id = request.GET.get('grade'))
    
    if not Class.objects.filter(name = request.GET.get('class')).exists:
        cls = Class.objects.get(name = request.GET.get('class'))
    else:
        cls = Class.objects.create(name = request.GET.get('class'), grade_number = request.GET.get('grade_number'))
        cls.save()

    #cls.grades.add(grade)
    source = Source.objects.get(id = 2)
    number = hamyar.scrape(cls, source, request.GET.get('link'))
    return HttpResponse(f"{number} questions scraped succesfully!")
   
@csrf_exempt
def bot(request):
  if request.method == 'POST':
    message = json.loads(request.body.decode('utf-8'))
    #print(json.dumps(message, indent=4))

    state = 0
    if message.get('message'):
      if message['message']['text'] != 'text' and (not User.objects.filter(user_id=message['message']['from']['id']).exists()):
        if (not User.objects.filter(user_id=message['message']['from']['id']).exists()):
            user = User.objects.create(user_id=message['message']['from']['id'], first_name= message['message']['from']['first_name'], last_name=message['message']['from']['last_name'])
        else: 
            user = User.objects.get(user_id=message['message']['from']['id'])
      else:
          user = User.objects.get(user_id=int(message['message']['from']['id']))
          state = user.state > 0
    
    
    if state:
      check_answer(message)
          
    elif message.get('callback_query') and message.get('callback_query')['data'][0] == "0":
        ask_role(message)
    elif message.get('callback_query') and message['callback_query']['data'][0] == "1":
        update_grade(message)
    elif message.get('callback_query') and message['callback_query']['data'][0] == "a":
        choose_unit(message, 0)
    elif message.get('callback_query') and message['callback_query']['data'][0] == "b":
        choose_unit(message, 1)
    elif message.get('callback_query') and message['callback_query']['data'][0] == "c":
        new_question(message, 1)
    elif message.get('callback_query') and message['callback_query']['data'][0] == "C":
        new_question(message, 0)
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
    elif message['message']['text'] == '/help':
        help(message['message']['chat']['id'])
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

def send_leaderboard(request):
    lead = ""
    number = 3
    ranking = [(user.score(), str(user)) for user in User.objects.all()]
    ranking = sorted(ranking, reverse=True)

    for i in range(1, number+1):
        lead += f"{persian.convert_en_numbers(i)}. {ranking[i-1][1]} ({persian.convert_en_numbers(ranking[i-1][0])} امتیاز)\n"
    
    send(
        'sendMessage',
        json.dumps({
            "chat_id": "6210855232",
            "text": strings.leaderboard.format(lead, persian.convert_en_numbers(number))
        })
    )

    return HttpResponse('ok')