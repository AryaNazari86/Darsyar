import requests
from bs4 import BeautifulSoup
#from content.models import Question, Unit

req = requests.get('https://hamgamdars.com/سوالات-متن-مطالعات-نهم/')
rqe = BeautifulSoup(req.text, 'html.parser')
rqe = req.select_one('#text-3 > main > article:nth-child(1) > div > div.accessibility-plugin-ac.entry-content.post > ol')
req = req.find_all('a')

strin = ""

for UN in range(1, 25):
    #unit = Unit.objects.get(id=UN)
    result = requests.get(web[UN-1]['href'])
    soup = BeautifulSoup(result.text, 'html.parser')

    soup = soup.find(attrs={'class': 'accessibility-plugin-ac entry-content post'})
    strin += soup.text

f = open("file.txt", "w")
f.write(strin)

