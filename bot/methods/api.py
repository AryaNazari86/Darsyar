import requests
from bot.credintials import TOKEN, API_URL, URL
from bot import strings


MENU = {
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
            "text": strings.MenuStrings.channel
          },
          {
            "text": strings.MenuStrings.support
          }
        ]]
      }

def send(method, data):
  return requests.post(API_URL + method, data).json()['result']['message_id']
