import json
import csv
from deep_translator import GoogleTranslator
from concurrent.futures import ThreadPoolExecutor, as_completed
from requests.exceptions import RequestException
import time
import random

def translate_batch(source, target, texts, max_retries=3):
    for attempt in range(max_retries):
        try:
            translator = GoogleTranslator(source=source, target=target)
            translations = translator.translate_batch(texts)
            return [t.lower() for t in translations]
        except (RequestException, Exception) as e:
            print(f"Error translating batch: {e}. Attempt {attempt + 1} of {max_retries}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt + random.random())  # Exponential backoff with jitter
            else:
                print("Max retries exceeded. Returning original texts.")
                return [text.lower() for text in texts]
            

print(translate_batch('fa', 'en', ['سلام خوبی چطوری', 'دیروز سوار موتور بوم', 'عبدوالقادر', 'سلاااااام', 'لطفا جواب این سوال رو بده']))