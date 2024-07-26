import requests
from bs4 import BeautifulSoup
from content.models import Question, Unit, Class, Source



def scrape(cls, source, link):
    counter = 0
    req = requests.get(link)
    req = BeautifulSoup(req.text, 'html.parser')
    req = req.find(attrs={'class': 'accessibility-plugin-ac entry-content post'})
    req = req.find_all('a')

    for UN in range(1, len(req) + 1):
        result = requests.get(req[UN - 1]['href'])
        soup = BeautifulSoup(result.text, 'html.parser')

        soup = soup.select_one('#text-3 > main > article:nth-child(1) > div > div.accessibility-plugin-ac.entry-content.post')
        name = soup.find(attrs={'class': 'center app-off more-off'})
        soup = soup.find_all('p')
        name = name.find_all('p')[-1].find('strong').text
        
        unit = Unit.objects.create(name = name, class_rel = cls)
        unit.save()
        
        
        for question in soup:
            if question.text.find('پاسخ:') == -1 and question.text.find('جواب:'):
                continue

            splitting_text = "پاسخ:" if question.text.find('پاسخ:') != -1 else "جواب:"
                
            counter += 1
            question = question.text.split(splitting_text)
            temp = question[0].split('-')
            if len(temp[0]) >= 5:
                temp = question[0].split('_')
            question[0] = ''
            for i in range(1, len(temp)):
                question[0] += temp[i]

            question = Question.objects.create(
                text=question[0], 
                answer=question[-1], 
                unit = unit, 
                source = source
            )
            question.save()

        
        print(f"unit {name} completed!")


    return counter
