import json
from user.models import User, UserQuestionRel
from content.models import Unit, Question
from bot import strings
from random import randint
import persian
from bot.AI import *
from .api import *
from .logs import *


def check_answer(message, chat_id, user_id):
    """send(
      'sendChatAction',
      json.dumps({
        "chat_id": message['message']['chat']['id'],
        "action": strings.making_pdf,
      })
    )"""

    user = User.objects.get(user_id=user_id)
    question = Question.objects.get(id=user.state)

    message_id = send(
        'sendMessage',
        json.dumps({
            "chat_id": chat_id,
            "text": strings.wait,
        })
    )

    req = ai(question.text, question.answer, message['message'].get('text'))

    if not UserQuestionRel.objects.filter(user=user, question=question).exists():
        pt = 100 * int(req['grade'])
        rel = UserQuestionRel.objects.create(
            user=user, question=question, point=pt)
        rel.save()
        user.calculated_score += pt
        user.save()

    send(
        'editMessageText',
        json.dumps({
            "chat_id": chat_id,
            "message_id": message_id,
            "text": strings.ai_answer.format(persian.convert_en_numbers(req['grade']), req['feedback'], question.answer),
            "reply_markup": MENU
        })
    )

    user.state = 0
    user.save()

    log_requests(user, question.unit, question.id, 2)


def switch_state(message, chat_id, user_id):
    # print(message['callback_query']['from']['id'])
    user = User.objects.get(user_id=user_id)
    user.state = int(message['callback_query']['data'][1:])
    user.save()

    send(
        'sendMessage',
        json.dumps({
            "chat_id": message['callback_query']['message']['chat']['id'],
            "text": strings.send_answer,
        })
    )

    question = Question.objects.get(
        id=int(message['callback_query']['data'][1:]))
    format = f"#AI {question.id}"
    send(
        'sendMessage',
        json.dumps({
            "chat_id": "5868778639",
            "text": strings.log.format(format, user, user.user_id, user.grade, question.unit.class_rel, question.unit.name, question),
        })
    )


def show_answer(message):
    question = Question.objects.get(
        id=int(message['callback_query']['data'][1:]))

    send(
        'editMessageText',
        json.dumps({
            "chat_id": message['callback_query']['message']['chat']['id'],
            "message_id": message['callback_query']['message']['message_id'],
            "text": strings.answer_text.format(question.text, question.answer),
            "reply_markup": {
                "inline_keyboard": [
                    [{
                        "text": strings.next_question,
                        "callback_data": "C" + str(question.unit.id),
                    }],
                    [{
                        "text": strings.show_help,
                        "callback_data": "6",
                    }]
                ]
            }
        })
    )


def new_question(message, first):
    unit = Unit.objects.all().get(
        id=int(message['callback_query']['data'][1:]))
    q = randint(0, unit.questions.count()-1)

    send(
        'sendPhoto',
        json.dumps({
            "chat_id": message['callback_query']['message']['chat']['id'],
            "from_chat_id": "@darsyarchannel",
            "message_id": message['callback_query']['message']['message_id'],
            "photo": "1274620264:1017637785560620802:0:4a16c9d0851906fefa6b055f138b54ae3c7b7805ace94705",
            "caption": strings.question.format(unit, unit.questions.all()[q].text),
            "reply_markup": {
                "inline_keyboard": [
                    [{
                        "text": strings.show_answer,
                        "callback_data": "4" + str(unit.questions.all()[q].id),
                    }],
                    [{
                        "text": strings.hint,
                        "callback_data": "h" + str(unit.questions.all()[q].id),
                    }],
                    [{
                        "text": strings.check_answer,
                        "callback_data": "5" + str(unit.questions.all()[q].id),
                    }],
                    [{
                        "text": strings.next_question,
                        "callback_data": "C" + str(unit.id),
                    }],
                    [{
                        "text": strings.show_help,
                        "callback_data": "6",
                    }]
                ]
            }
        })
    )

    if first:
        send(
            "deleteMessage",
            json.dumps({
                "chat_id": message['callback_query']['message']['chat']['id'],
                "message_id": message['callback_query']['message']['message_id'],
            })
        )

    user = User.objects.get(user_id=message['callback_query']['from']['id'])

    log_requests(user, unit, unit.questions.all()[q].id, 0)

def get_hint(message, chat_id, user_id):
    message_id = send(
        'sendMessage',
        json.dumps({
            "chat_id": chat_id,
            "text": strings.wait
        })
    )

    question = Question.objects.get(
        id=int(message['callback_query']['data'][1:])
    )

    if question.hint == None:
        question.hint = hint(question.text, question.answer)
        question.save()
    
    send(
        'deleteMessage',
        json.dumps({
            "chat_id": chat_id,
            "message_id": message_id,
        })
    )

    send(
        'editMessageText',
        json.dumps({
            "chat_id": chat_id,
            "message_id": message['callback_query']['message']['message_id'],#message_id,
            "text": strings.show_hint.format(question.text, question.hint),
            "reply_markup": {
                "inline_keyboard": [
                    [{
                        "text": strings.show_answer,
                        "callback_data": "4" + str(question.id),
                    }],
                    [{
                        "text": strings.check_answer,
                        "callback_data": "5" + str(question.id),
                    }],
                    [{
                        "text": strings.next_question,
                        "callback_data": "C" + str(question.unit.id),
                    }],
                    [{
                        "text": strings.show_help,
                        "callback_data": "6",
                    }]
                ]
            }
        })
    )

    user = User.objects.get(user_id = user_id)

    log_requests(user, question.unit, question.id, 3)