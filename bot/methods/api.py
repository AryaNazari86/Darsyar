import requests
from bot.credintials import PLATFORM, TOKEN, API_URL, URL
from bot import strings
import json

MENU = json.dumps({
    "keyboard": [
        [
            {
                "text": strings.MenuStrings.new_question
            },
        ],
        [
            {
                "text": strings.MenuStrings.new_test
            },
        ],
        [
            {
                "text": strings.MenuStrings.change_grade
            },
            {
                "text": strings.MenuStrings.show_score
            },
        ],
        [
            {
                "text": strings.MenuStrings.invite
            },
            {
                "text": strings.MenuStrings.support
            }
        ],
        ]
})


def send(method, data):
    req = requests.post(
        API_URL + method,
        data
    ).json()

    #print(json.dumps(req, indent = 4))
    

    try:
        return req['result']['message_id']
    except:
        return req
