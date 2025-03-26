import json
from bot.credintials import DARSYAR_QUESTION_FILE_ID, PLATFORM
from user.models import User, UserQuestionRel
from content.models import Unit, Question
from bot import strings
from random import randint
import persian
from bot.AI import *
from .api import *
from .logs import *
from ..AI import tutor


def ask_tutor(message, chat_id):
    message_id = send(
        'sendMessage',
        {
            "chat_id": chat_id,
            "text": strings.wait
        }
    )

    text = message['message']['text']

    response = tutor(text)

    response += "\n\n⚠️ مسئولیت محتوای تولید شده برعهده کاربر است."
    
    send(
        'deleteMessage',
        {
            "chat_id": chat_id,
            "message_id": message_id,
        }
    )

    send(
        'sendMessage',
        {
            "chat_id": chat_id,
            "text": response,
            "reply_markup": MENU,
        }
    )

    #user = User.objects.get( platform = PLATFORM,user_id = user_id)

    #log_requests(user, question.unit, question.id, 3)