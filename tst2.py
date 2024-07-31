import requests
import json

url = "https://tapi.bale.ai/bot1606650841:2JdOjsHHNT9XkO76VH8UwsKn4o9KFuY4kB4YQyUF/sendMessage"
headers = {"Content-Type": "application/json"}

data = {
    "chat_id": 2130762647,
    "text": "hello",
    "reply_markup": {
        "keyboard": [
        [
          {
            "text": "hello"
          },
        ]]
      }
}

response = requests.post(url, headers=headers, data=json.dumps(data))

if response.status_code == 200:
    print("Message sent successfully")
else:
    print(f"Failed to send message. Response code: {response.status_code}, message: {response.text}")