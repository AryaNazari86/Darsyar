import requests
import json

def ai(question, real_answer, user_answer):
    url = "https://darsyarai.pythonanywhere.com/v1/chat/completions"

    payload = json.dumps({
        "model": "gemini-1.5-flash",
        "tempature": 1,
        "question": question,
        "realAnswer": real_answer,
        "userAnswer": user_answer
    })
    
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()

def hint(question, answer):
    url = "https://darsyarai.pythonanywhere.com/v1/hint"

    payload = json.dumps({
        "model": "gemini-1.5-flash",
        "tempature": 1,
        "question": question,
        "answer": answer
    })
    
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.text
