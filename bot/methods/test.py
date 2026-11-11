import json
from django.http import FileResponse, HttpResponse
from weasyprint import HTML
from bot.credintials import PLATFORM
from content.models import Unit
from django.shortcuts import render
from persiantools.jdatetime import JalaliDateTime
import pytz
import random
from .logs import log_requests
from user.models import User
from .api import *


def get_html(request, unit_id):
    try:
        unit = Unit.objects.all().get(id=int(unit_id))
        questions = list(unit.questions.all())
        random_questions = random.sample(questions, min(5, len(questions)))
        random_questions_objects = [
            {
                'text': question.text,
                'answer': question.answer,
                'sourceText': question.source.name if question.source else None
            }
            for question in random_questions
        ]
        return render(request, 'exam.html', {"questions": random_questions_objects, "unit": unit.class_rel.name, "date": JalaliDateTime.now(pytz.utc).strftime("%Y/%m/%d")})
    except Exception as e:
        print(e)
        return HttpResponse('ok')


def new_test(message, url, user_id):
    chat_id = message['callback_query']['message']['chat']['id']
    wait_message_id = message['callback_query']['message']['message_id']

    send(
        'editMessageText',
        {
            "chat_id": chat_id,
            "message_id": wait_message_id,
            "text": strings.wait,
        }
    )

    # print(message['callback_query']['data'])
    unit = Unit.objects.all().get(
        id=int(message['callback_query']['data'][1:]))

    try:
        pdf = HTML(url=f'{url}gethtml/{unit.id}').write_pdf()
    except Exception as e:
        print(f"exam pdf render failed for unit {unit.id}: {e}", flush=True)
        send(
            'editMessageText',
            {
                "chat_id": chat_id,
                "message_id": wait_message_id,
                "text": strings.test_failed,
                "reply_markup": MENU,
            }
        )
        return

    user = User.objects.get(
        platform=PLATFORM, user_id=message['callback_query']['from']['id'])

    # The PDF goes up as multipart. It used to be parked on tmpfiles.org and
    # handed over as a URL, but their /dl/ links now 302 to an HTML landing
    # page, so the platform fetched that page instead of the file and the user
    # got nothing.
    result = send(
        'sendDocument',
        {
            "chat_id": chat_id,
            "reply_markup": MENU,
            "caption": strings.test_caption.format(user.grade.name, unit.class_rel.name, unit.name),
        },
        files={'document': ('exam.pdf', pdf, 'application/pdf')},
    )

    # send() returns the new message_id on success and the raw API response
    # otherwise; without this check a rejected upload looked like a success.
    if not isinstance(result, int):
        print(f"sendDocument failed for unit {unit.id}: {result}", flush=True)
        send(
            'editMessageText',
            {
                "chat_id": chat_id,
                "message_id": wait_message_id,
                "text": strings.test_failed,
                "reply_markup": MENU,
            }
        )
        return

    send(
        'deleteMessage',
        {
            "chat_id": chat_id,
            "message_id": wait_message_id,
        }
    )

    log_requests(user, unit, 0, 1)