import requests
from bs4 import BeautifulSoup
from content.models import Question, Unit
result = requests.get('https://hamgamdars.com/سوالات-درس-1-مطالعات-نهم/')
soup = BeautifulSoup(result.text, 'html.parser')

soup = soup.select_one('#text-3 > main > article:nth-child(1) > div > div.accessibility-plugin-ac.entry-content.post')

soup = soup.find_all('p')

unit = Unit.objects.get(id = 1)


for i in soup[7:30]:
    q = i.get_text(strip=True, separator='<br/>').split('<br/>')
    
    s = q[0].split('-')
    q[0] = ''
    for j in s[1:]:
        q[0] += j
    print(q[0])
    print(q[-1])
    question = Question.objects.create(text=q[0], answer=q[-1], unit=unit, source = source)

