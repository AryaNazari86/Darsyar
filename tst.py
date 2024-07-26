import requests
from bs4 import BeautifulSoup
#from content.models import Question, Unit

req = requests.get('https://hamgamdars.com/سوالات-متن-مطالعات-نهم/')
req = BeautifulSoup(req.text, 'html.parser')
req = req.select_one('#text-3 > main > article:nth-child(1) > div > div.accessibility-plugin-ac.entry-content.post > ol')
req = req.find_all('a')

strin = ""

for UN in range(24, 25):
    #unit = Unit.objects.get(id=UN)
    result = requests.get(req[UN-1]['href'])
    soup = BeautifulSoup(result.text, 'html.parser')

    

    soup = soup.find(attrs={'class': 'accessibility-plugin-ac entry-content post'})
    name = soup.find(attrs={'class': 'center app-off more-off'})
    name = name.find_all('p')[-1].find('strong').text
    question = soup.find_all('p')[33].text.split('پاسخ:')
    temp = question[0].split('-')
    if len(temp[0]) >= 5:
        temp = question[0].split('_')
    question[0] = ''
    for i in range(1, len(temp)):
        question[0] += temp[i]
    print(question[0], question[-1])



