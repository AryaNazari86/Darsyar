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
from django.shortcuts import render
from django.db.models.functions import TruncDate
from django.db.models import Count, Q
import matplotlib
import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime, timedelta

# Use the 'Agg' backend for non-GUI environments
matplotlib.use('Agg')

def plot_overall_usage(request):
    # Group logs by date and type
    datewise_logs = LOG.objects.annotate(date=TruncDate('date_created')).values('date').annotate(
        total=Count('id'),
        questions=Count('id', filter=Q(type=0)),
        tests=Count('id', filter=Q(type=1)),
        ai=Count('id', filter=Q(type=2))
    ).order_by('date')

    # Extract data for plotting
    dates = [entry['date'] for entry in datewise_logs]
    totals = [entry['total'] for entry in datewise_logs]
    questions = [entry['questions'] for entry in datewise_logs]
    tests = [entry['tests'] for entry in datewise_logs]
    ai = [entry['ai'] for entry in datewise_logs]

    # Plot overall usage with detailed styling
    plt.figure(figsize=(16, 10))
    plt.plot(dates, totals, label='Total Logs', color='black', linestyle='-', linewidth=2, marker='o')
    plt.plot(dates, questions, label='Questions', color='blue', linestyle='--', linewidth=2, marker='x')
    plt.plot(dates, tests, label='Tests', color='green', linestyle='-.', linewidth=2, marker='s')
    plt.plot(dates, ai, label='AI', color='red', linestyle=':', linewidth=2, marker='d')

    plt.grid(color='gray', linestyle='--', linewidth=0.5)
    plt.title('Overall App Usage Over Time', fontsize=24, fontweight='bold')
    plt.xlabel('Date', fontsize=18)
    plt.ylabel('Number of Logs', fontsize=18)
    plt.xticks(rotation=45, fontsize=14)
    plt.yticks(fontsize=14)
    plt.legend(fontsize=14)

    # Highlight the peak day with annotation
    if totals:
        peak_day = dates[totals.index(max(totals))]
        peak_value = max(totals)
        plt.annotate(f'Peak: {peak_value} logs', xy=(peak_day, peak_value), xytext=(peak_day, peak_value + 5),
                     arrowprops=dict(facecolor='black', shrink=0.05), fontsize=12, ha='center')

    # Add annotations for growth
    for i in range(1, len(totals)):
        growth = ((totals[i] - totals[i-1]) / totals[i-1]) * 100 if totals[i-1] > 0 else 0
        plt.annotate(f'{growth:+.2f}%', (dates[i], totals[i]), textcoords="offset points", xytext=(0,10), ha='center', fontsize=10)

    # Save plot to a PNG image in memory
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    overall_image_png = buffer.getvalue()
    buffer.close()

    # Encode image to base64 string
    overall_graph = base64.b64encode(overall_image_png).decode('utf-8')

    # Calculate insights
    total_logs = sum(totals)
    avg_logs_per_day = sum(totals) / len(totals) if totals else 0
    peak_day = dates[totals.index(max(totals))] if totals else None
    peak_count = max(totals) if totals else 0

    # Determine numerical growth or decline by comparing first and last week
    if len(totals) > 7:
        first_week_avg = sum(totals[:7]) / 7
        last_week_avg = sum(totals[-7:]) / 7
        growth_percentage = ((last_week_avg - first_week_avg) / first_week_avg) * 100 if first_week_avg > 0 else 0
    else:
        growth_percentage = 0

    # Prepare context with the graph and insights
    context = {
        'overall_graph': overall_graph,
        'total_logs': total_logs,
        'avg_logs_per_day': avg_logs_per_day,
        'peak_day': peak_day,
        'peak_count': peak_count,
        'growth_percentage': growth_percentage,
    }

    return render(request, 'overall_usage.html', context)
from django.shortcuts import render
from django.db.models.functions import TruncDate
from django.db.models import Count
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import io
import base64
from datetime import datetime

# Use the 'Agg' backend for non-GUI environments
matplotlib.use('Agg')

def plot_user_creation_trends(request):
    try:
        # Group users by date_created
        datewise_users = User.objects.annotate(date=TruncDate('date_created')).values('date').annotate(
            total_users=Count('user_id')
        ).order_by('date')

        # Extract data for plotting
        dates = [entry['date'] for entry in datewise_users]
        total_users = [entry['total_users'] for entry in datewise_users]

        # Ensure there is data to plot
        if not dates:
            return render(request, 'user_creation_trends.html', {'user_creation_graph': None})

        # Plot user creation trends
        plt.figure(figsize=(16, 10))
        plt.plot(dates, total_users, label='User Registrations', color='purple', linestyle='-', linewidth=2, marker='o')

        # Set the x-axis limits to match the range of dates
        plt.xlim(min(dates), max(dates))

        # Formatting the x-axis with dynamic date range
        ax = plt.gca()
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

        plt.grid(color='gray', linestyle='--', linewidth=0.5)
        plt.title('User Creation Trends Over Time', fontsize=24, fontweight='bold')
        plt.xlabel('Date', fontsize=18)
        plt.ylabel('Number of Users', fontsize=18)
        plt.xticks(fontsize=14, rotation=45)  # Rotate dates for better readability
        plt.yticks(fontsize=14)
        plt.legend(fontsize=14)

        # Highlight the peak day with annotation
        peak_day = dates[total_users.index(max(total_users))]
        peak_value = max(total_users)
        plt.annotate(f'Peak: {peak_value} users', xy=(peak_day, peak_value), xytext=(peak_day, peak_value + 2),
                     arrowprops=dict(facecolor='black', shrink=0.05), fontsize=12, ha='center')

        # Save plot to a PNG image in memory
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        user_creation_image_png = buffer.getvalue()
        buffer.close()

        # Encode image to base64 string
        user_creation_graph = base64.b64encode(user_creation_image_png).decode('utf-8')

        # Calculate insights
        total_users_count = sum(total_users)
        avg_users_per_day = sum(total_users) / len(total_users) if total_users else 0
        peak_day = dates[total_users.index(max(total_users))] if total_users else None
        peak_count = max(total_users) if total_users else 0

        # Prepare context with the graph and insights
        context = {
            'user_creation_graph': user_creation_graph,
            'total_users_count': total_users_count,
            'avg_users_per_day': avg_users_per_day,
            'peak_day': peak_day,
            'peak_count': peak_count,
        }

        return render(request, 'user_creation_trends.html', context)

    except Exception as e:
        # Log the exception (optional)
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error plotting user creation trends: {e}")

        # Return a response with an error message
        return render(request, 'user_creation_trends.html', {'user_creation_graph': None, 'error_message': str(e)})
