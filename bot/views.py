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
from django.shortcuts import render
from django.db.models.functions import ExtractHour
from django.db.models import Count
import matplotlib
import matplotlib.pyplot as plt
import io
from datetime import timedelta
import base64
from django.shortcuts import render
from django.db.models.functions import ExtractHour, ExtractMinute
from django.db.models import Count
from django.utils.timezone import now
import matplotlib
import matplotlib.pyplot as plt
import io
import base64
from datetime import timedelta


def scraper(request):
    # grade = Grade.objects.filter(id = request.GET.get('grade'))

    if not Class.objects.filter(name=request.GET.get('class')).exists:
        cls = Class.objects.get(name=request.GET.get('class'))
    else:
        cls = Class.objects.create(name=request.GET.get(
            'class'), grade_number=request.GET.get('grade_number'))
    # cls.grades.add(grade)
    source = Source.objects.get(id=1)
    number = scrape(cls, source, request.GET.get('link'))
    return HttpResponse(f"{number} questions scraped succesfully!")


def scrape_hamyar(request):
    # grade = Grade.objects.filter(id = request.GET.get('grade'))

    if not Class.objects.filter(name=request.GET.get('class')).exists:
        cls = Class.objects.get(name=request.GET.get('class'))
    else:
        cls = Class.objects.create(name=request.GET.get(
            'class'), grade_number=request.GET.get('grade_number'))
        cls.save()

    # cls.grades.add(grade)
    source = Source.objects.get(id=2)
    number = hamyar.scrape(cls, source, request.GET.get('link'))
    return HttpResponse(f"{number} questions scraped succesfully!")


@csrf_exempt
def bot(request):
    try:
        if request.method == 'POST':
            message = json.loads(request.body.decode('utf-8'))
            # print(message)
            try:
                user_id = message.get('message').get('from').get('id')
            except:
                user_id = message.get('callback_query').get('from').get('id')

            # Check If user has subscribed
            req = requests.post(
                API_URL + "getChatMember",
                json.dumps({
                    "chat_id": "5557386819",
                    "user_id": user_id
                })
            ).json()

            if req['ok'] == False:
                join_channel(message)
                return HttpResponse('ok')

            # print(json.dumps(message, indent=4))

            state = 0
            if message.get('message') and message['message'].get('text'):
                if message['message']['text'] != 'text' and (not User.objects.filter(user_id=message['message']['from']['id']).exists()):
                    if (not User.objects.filter(user_id=message['message']['from']['id']).exists()):
                        user = User.objects.create(user_id=message['message']['from']['id'], first_name=message['message']
                                                   ['from']['first_name'], last_name=message['message']['from']['last_name'])
                    else:
                        user = User.objects.get(
                            user_id=message['message']['from']['id'])
                else:
                    user = User.objects.get(user_id=int(
                        message['message']['from']['id']))
                    state = user.state > 0

            if state:
                check_answer(message)

            elif message.get('callback_query') and message.get('callback_query')['data'] == "-":
                start(message)
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

            elif message.get('message') and message['message'].get('text') == '/start':
                start(message)
            elif message.get('message') and message['message'].get('text') == '/help':
                help(message['message']['chat']['id'])
            elif message.get('message') and message['message'].get('text') == strings.MenuStrings.new_question or message['message'].get('text') == '/question':
                choose_class(message, 0)
            elif message.get('message') and message['message'].get('text') == strings.MenuStrings.new_test or message['message'].get('text') == '/test':
                choose_class(message, 1)
            elif message.get('message') and message['message'].get('text') == strings.MenuStrings.show_score:
                show_score(message)
            elif message.get('message') and message['message'].get('text') == strings.MenuStrings.change_grade:
                new_grade(message)
            elif message.get('message') and message['message'].get('text') == strings.MenuStrings.channel:
                channel(message)
            elif message.get('message') and message['message'].get('text') == strings.MenuStrings.support:
                support(message)

            else:
                Sticker(message)

        return HttpResponse('ok')
    except Exception as e:
        print(e)
        return HttpResponse('ok')


def bale_setwebhook(request):
    response = requests.post(
        API_URL + "setWebhook?url=" + request.build_absolute_uri('/')).json()
    return HttpResponse(f"{response}")


def send_leaderboard(request, number):
    lead = ""
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

    return HttpResponse(lead)


matplotlib.use('Agg')


def plot_logs_by_hour(request):
    try:
        # Group by the hour of the day
        log_data = LOG.objects.annotate(hour=ExtractHour('date_created')).values(
            'hour').annotate(count=Count('id')).order_by('hour')

        # Extract hours and counts
        hours = [entry['hour'] for entry in log_data]
        counts = [entry['count'] for entry in log_data]

        # Calculate insights
        total_logs = sum(counts)
        peak_hour = hours[counts.index(max(counts))] if counts else None
        peak_count = max(counts) if counts else 0

        # Current time span
        current_time = now()
        start_time = current_time - timedelta(minutes=5)
        end_time = current_time + timedelta(minutes=5)

        # Logs in the 5-minute span
        logs_in_time_span = LOG.objects.filter(
            date_created__range=(start_time, end_time)).count()

        # Enhanced Plotting
        plt.figure(figsize=(12, 8))
        plt.plot(hours, counts, color='#1f77b4', marker='o',
                 linestyle='-', linewidth=2, markersize=8)
        plt.grid(color='gray', linestyle='--', linewidth=0.5)
        plt.title('Number of Logs per Hour', fontsize=20, fontweight='bold')
        plt.xlabel('Hour of the Day', fontsize=16)
        plt.ylabel('Number of Logs', fontsize=16)
        plt.xticks(range(24), fontsize=12)
        plt.yticks(fontsize=12)

        # Annotate data points with counts
        for i, txt in enumerate(counts):
            plt.annotate(txt, (hours[i], counts[i]), textcoords="offset points", xytext=(
                0, 5), ha='center', fontsize=10)

        # Save plot to a PNG image in memory
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()

        # Encode image to base64 string
        graph = base64.b64encode(image_png)
        graph = graph.decode('utf-8')

        # Prepare context with insights
        context = {
            'graph': graph,
            'total_logs': total_logs,
            'peak_hour': peak_hour,
            'peak_count': peak_count,
            'logs_in_time_span': logs_in_time_span,
            'current_time': current_time,
        }

        return render(request, 'logs_by_hour.html', context)
    except Exception as e:
        return HttpResponse(e)
