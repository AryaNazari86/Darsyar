import requests
from bs4 import BeautifulSoup
from content.models import Question, Unit, Class, Source

st = 776

def scrape(cls, source, link):
    counter = 0
    req = requests.get(link)
    req = BeautifulSoup(req.text, 'html.parser')
    req = req.select_one('#block-post > div.post > div.post-content > ol')
    req = req.find_all('a')
    

    for UN in range(1, len(req) + 1):
        result = requests.get(req[UN - 1]['href'])
        soup1 = BeautifulSoup(result.text, 'html.parser')

        soup = soup1.select_one('#block-post > div.post > div.post-content')
        try:
            name = soup1.select_one('#block-post > div.post > div.post-content > p:nth-child(4)').text.split(':')[-1].strip() 
        except:
            name = f'درس {UN}'
        soup = soup.find_all('p')
        #name = name.text.split(':')[-1].strip() #find_all('p')[-1].find('strong').text
        
        #unit = Unit.objects.get(id = UN + st - 1) 
        if (len(name) > 50):
            name = f'درس {UN}'
        unit = Unit.objects.create(name = name, class_rel = cls) 
        unit.save()
        
        counter2 = 0
        for question in soup:
            if question.text.find('پاسخ:') == -1 and question.text.find('جواب:') == -1:
                continue

            splitting_text = "پاسخ:" if question.text.find('پاسخ:') != -1 else "جواب:"
                
            counter2 += 1
            question = question.text.split(splitting_text)
        
            temp = question[0].split('ـ')
            if len(temp[0]) >= 5:
                temp = question[0].split('-')
            
            question[0] = ''
            for i in range(1 if len(temp) > 1 else 0, len(temp)):
                question[0] += temp[i]

            question = Question.objects.create(
                text=question[0].strip(), 
                answer=question[-1].strip(), 
                unit = unit, 
                source = source
            )

            question.save()

        
        counter += counter2 
        #print(counter)
        print(f"unit {unit.name} completed!")


    return counter

