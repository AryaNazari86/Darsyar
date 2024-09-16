import matplotlib.dates as mdates
import json
import requests
import matplotlib
import matplotlib.pyplot as plt
import io
import base64
import persian
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from bot.credintials import TOKEN, API_URL, URL
from user.models import User, UserQuestionRel
from content.models import Grade, Class, Unit, Question, Source
from bot import strings
from django.shortcuts import render
from .methods.general import *
from .methods.test import *
from .methods.question import *
from .methods.settings import *
from .scraper import scrape
from . import hamyar
from datetime import datetime
from django.shortcuts import render
from django.db.models.functions import TruncDate
from django.db.models import Count, Q
from django.db.models.functions import ExtractHour, ExtractMinute
from datetime import datetime, timedelta
from django.utils.timezone import now
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Count
import matplotlib.pyplot as plt
import io
import base64
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
from django.db import models  # Import models here
from .credintials import BOT_USERNAME, CHANNEL_ID, PLATFORM
from bot.methods.note import *

matplotlib.use('Agg')


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
            print(json.dumps(message, indent=4))        

            # Fetch data related to the message
            try:
                user_id = message['message']['from']['id']
                chat_id = message['message']['chat']['id']
                msg = message['message']
                type = 0
            except:
                user_id = message['callback_query']['from']['id']
                chat_id = message['callback_query']['message']['chat']['id']
                msg = message['callback_query']['message']
                type = 1

            if (user_id != chat_id) and (type == 0) and not (BOT_USERNAME in message['message'].get('text')):
                return HttpResponse('ok')
                

            state = 0

            if (not User.objects.filter(user_id=user_id, platform=PLATFORM).exists()):
                user = User.objects.create(
                    id = PLATFORM + "_" + str(user_id) if (PLATFORM == "TG") else str(user_id) ,
                    platform = PLATFORM,
                    user_id=user_id,
                    first_name=msg['from']['first_name'],
                )
                user.save()

                if type == 0 and msg.get('text')[:6] == '/start':
                    add_invite(user_id, msg.get('text')[7:])

            else:
                user = User.objects.get(
                    platform = PLATFORM,
                    user_id=user_id
                )

                state = user.state

            # Check is user has joined the channel
            req = requests.post(
                API_URL + "getChatMember",
                {
                    "chat_id": CHANNEL_ID,
                    "user_id": user_id
                }
            ).json()

            if req['ok'] == False or (req['result']['status'] in ("left", "banned", "restricted")):
                join_channel(chat_id)
                return HttpResponse('ok')


            if state > 0:
                check_answer(message, chat_id, user_id)
            elif message.get('callback_query') and message.get('callback_query')['data'] == "^":
                reset_state(chat_id, user_id)
            elif state < 0:
                receive_note(chat_id, user_id, msg)

            elif message.get('callback_query') and message.get('callback_query')['data'][0] == "@":
                report(chat_id, msg, message['callback_query']['data'][1:])
            elif message.get('callback_query') and message.get('callback_query')['data'] == "!":
                help(chat_id)
            elif message.get('callback_query') and message.get('callback_query')['data'] == "-":
                start(chat_id, user_id)
            elif message.get('callback_query') and message['callback_query']['data'][0] == "&":
                upvote_note(chat_id, user_id, message['callback_query']['data'][1:])
            elif message.get('callback_query') and message['callback_query']['data'][0] == "*":
                downvote_note(chat_id, user_id, message['callback_query']['data'][1:])
            elif message.get('callback_query') and message.get('callback_query')['data'][0] == "0":
                ask_role(message, user_id)
            elif message.get('callback_query') and message['callback_query']['data'][0] == "1":
                update_grade(message, user_id)
            elif message.get('callback_query') and message['callback_query']['data'][0] == "a":
                choose_unit(message, 0)
            elif message.get('callback_query') and message['callback_query']['data'][0] == "b":
                choose_unit(message, 1)
            elif message.get('callback_query') and message['callback_query']['data'][0] == "n":
                send_note(chat_id, message['callback_query']['data'][1:])
            elif message.get('callback_query') and message['callback_query']['data'][0] == "m":
                add_note(chat_id, user_id, message['callback_query']['data'][1:])
            elif message.get('callback_query') and message['callback_query']['data'][0] == "c":
                new_question(message, 1, user_id)
            elif message.get('callback_query') and message['callback_query']['data'][0] == "C":
                new_question(message, 0, user_id)
            elif message.get('callback_query') and message['callback_query']['data'][0] == "d":
                new_test(message, request.build_absolute_uri('/'), user_id)
            elif message.get('callback_query') and message['callback_query']['data'][0] == "h":
                get_hint(message, chat_id, user_id)
            elif message.get('callback_query') and message['callback_query']['data'][0] == "4":
                show_answer(message)
            elif message.get('callback_query') and message['callback_query']['data'][0] == "5":
                switch_state(message, chat_id, user_id)
            elif message.get('callback_query') and message['callback_query']['data'][0] == "6":
                help(chat_id)

            elif message.get('message') and message['message'].get('text')[0:6] == '/start':
                start(chat_id, user_id)
            elif message.get('message') and message['message'].get('text') == '/help':
                help(message['message']['chat']['id'])
            elif message.get('message') and message['message'].get('text') == strings.MenuStrings.new_question or message['message'].get('text') == '/question':
                choose_class(message, 0, chat_id, user_id)
            elif message.get('message') and message['message'].get('text') == strings.MenuStrings.new_test or message['message'].get('text') == '/test':
                choose_class(message, 1, chat_id, user_id)
            elif message.get('message') and message['message'].get('text') == strings.MenuStrings.note or message['message'].get('text') == '/note':
                choose_class_note(chat_id, user_id)
            elif message.get('message') and message['message'].get('text') == strings.MenuStrings.addnote or message['message'].get('text') == '/addnote':
                choose_class_addnote(chat_id, user_id)
            elif message.get('message') and message['message'].get('text') == strings.MenuStrings.show_score:
                show_score(message, chat_id, user_id)
            elif message.get('message') and message['message'].get('text') == strings.MenuStrings.change_grade:
                new_grade(chat_id)
            #elif message.get('message') and message['message'].get('text') == strings.MenuStrings.channel:
            #    channel(chat_id)
            elif message.get('message') and message['message'].get('text') == strings.MenuStrings.support:
                support(chat_id)
            elif message.get('message') and message['message'].get('text') == strings.MenuStrings.invite:
                send_invite(user_id, chat_id)

            else:
                Sticker(chat_id)

        return HttpResponse('ok')

    except Exception as e:
        print(e)
        return HttpResponse('ok')


def setwebhook(request):
    response = requests.post(
        API_URL + "setWebhook?url=" + request.build_absolute_uri('/').replace('http', 'https')
    ).json()

    # print(API_URL + "setWebhook?url=" + request.build_absolute_uri('/'))

    return HttpResponse(f"{response}")


def send_leaderboard(request, number):
    result = ""
    ranking = User.objects.order_by('calculated_score').reverse()

    for i in range(1, number+1):
        result += f"{persian.convert_en_numbers(i)}. {str(ranking[i-1])} ({persian.convert_en_numbers(ranking[i-1].calculated_score)} امتیاز)\n"

    send(
        'sendMessage',
        {
            "chat_id": "6210855232",
            "text": strings.leaderboard.format(result, persian.convert_en_numbers(number))
        }
    )

    return HttpResponse(result)


def plot_logs_by_hour(request):
    try:
        # Log types
        log_types = {
            0: 'Question',
            1: 'Test',
            2: 'AI',
        }

        peak_count = 0
        peak_hour = 0

        # Initialize data for each log type
        log_data_by_type = {}
        for log_type, label in log_types.items():
            log_data_by_type[label] = LOG.objects.filter(type=log_type).annotate(hour=models.functions.ExtractHour('date_created')).values('hour').annotate(count=Count('id')).order_by('hour')

        # Sum all types for the combined line
        combined_counts = {}
        for log_data in log_data_by_type.values():
            for entry in log_data:
                hour = entry['hour']
                count = entry['count']
                if hour in combined_counts:
                    combined_counts[hour] += count
                else:
                    combined_counts[hour] = count

        combined_hours = sorted(combined_counts.keys())
        combined_count_values = [combined_counts[hour] for hour in combined_hours]

        # Calculate insights
        total_logs = sum(combined_count_values)
        peak_hour = None
        peak_count = 0

        # Plotting
        plt.figure(figsize=(12, 8))
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c']  # Different colors for each log type

        for i, (label, log_data) in enumerate(log_data_by_type.items()):
            hours = [entry['hour'] for entry in log_data]
            counts = [entry['count'] for entry in log_data]

            # Update peak hour and count if needed
            
            # Plot each log type with smaller lines
            plt.plot(hours, counts, color=colors[i], marker='o', linestyle='-', linewidth=1.5, markersize=6, label=f'{label} Logs')

            # Annotate data points with counts
            for j, txt in enumerate(counts):
                plt.annotate(txt, (hours[j], counts[j]), textcoords="offset points", xytext=(0, 5), ha='center', fontsize=10)

        # Plot the combined line with a bolder style
        plt.plot(combined_hours, combined_count_values, color='black', marker='o', linestyle='-', linewidth=3, markersize=8, label='All Logs')

        # Annotate the combined line data points with counts
        for i, txt in enumerate(combined_count_values):
            plt.annotate(txt, (combined_hours[i], combined_count_values[i]), textcoords="offset points", xytext=(0, 5), ha='center', fontsize=10, color='black')
            if combined_count_values[i] > peak_count:
                peak_hour = combined_hours[i]
                peak_count = combined_count_values[i]

        plt.grid(color='gray', linestyle='--', linewidth=0.5)
        plt.title('Number of Logs per Hour by Type and Combined', fontsize=20, fontweight='bold')
        plt.xlabel('Hour of the Day', fontsize=16)
        plt.ylabel('Number of Logs', fontsize=16)
        plt.xticks(range(24), fontsize=12)
        plt.yticks(fontsize=12)
        plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        plt.legend(fontsize=12)

        #peak_count = max(combined_counts)
        #peak_hour = combined_hours[combined_counts.index(peak_count)]
        
        # Save plot to a PNG image in memory
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()

        # Encode image to base64 string
        graph = base64.b64encode(image_png).decode('utf-8')

        # Current time span for +/- 5 minutes
        current_time = now()
        start_time = current_time - timedelta(minutes=5)
        end_time = current_time + timedelta(minutes=5)
        logs_in_time_span = LOG.objects.filter(date_created__range=(start_time, end_time)).count()

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
