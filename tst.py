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

def process_question_batch(source_lang, target_lang, questions):
    texts = [item for sublist in questions for item in sublist]
    translations = translate_batch(source_lang, target_lang, texts)
    num_texts_per_question = 2
    return [translations[i:i + num_texts_per_question] for i in range(0, len(translations), num_texts_per_question)]

def load_data(file_path):
    grades = {}
    classes = {}
    units = {}
    questions = []
    
    with open(file_path) as f:
        data = json.load(f)
        for i in data:
            if i['model'] == 'content.question':
            
                questions.append([
                    i['fields']['text'],
                    i['fields']['answer'] or '',
                ])
    
    return questions

def main():
    source_lang = 'fa'  # Persian
    target_lang = 'en'  # English
    batch_size = 50  # Adjust batch size as needed
    
    questions = load_data('data.json')
    total_rows = len(questions)

    with open('data3.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Question', 'Answer'])

        with ThreadPoolExecutor(max_workers=3) as executor:  # Reduce number of threads
            futures = []
            for i in range(0, total_rows, batch_size):
                batch = questions[i:i + batch_size]
                futures.append(executor.submit(process_question_batch, source_lang, target_lang, batch))
                print(f"Submitted batch {i // batch_size + 1} for processing.")

            for i, future in enumerate(as_completed(futures)):
                results = future.result()
                writer.writerows(results)
                print(f"Wrote {min((i + 1) * batch_size, total_rows)} out of {total_rows} rows to CSV.")

if __name__ == "__main__":
    main()
