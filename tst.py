import requests
from bs4 import BeautifulSoup
#from content.models import Question, Unit

hamgam = requests.get('https://hamgamdars.com/سوالات-متن-مطالعات-نهم/')
web = BeautifulSoup(hamgam.text, 'html.parser')
web = web.select_one('#text-3 > main > article:nth-child(1) > div > div.accessibility-plugin-ac.entry-content.post > ol')
web = web.find_all('a')
print(len(web))

for UN in range(24, 25):
    #unit = Unit.objects.get(id=UN)
    result = requests.get(web[UN-1]['href'])
    soup = BeautifulSoup(result.text, 'html.parser')

    soup = soup.find(attrs={'class': 'accessibility-plugin-ac entry-content post'})
    #select_one('#text-3 > main > article:nth-child(1) > div > div.accessibility-plugin-ac.entry-content.post')

    soup = soup.find_all('p')
    print(soup[3])
    print(soup[3].find('strong').text)
    
    soup[5].find('strong').decompose()
    print(UN, soup[5].text.split('::')[-1])
    for i in soup[7:]:
        q = i.get_text(strip=True, separator='<br/>').split('<br/>')
        
        s = q[0].split('-')
        if len(s) <= 1:
            continue
        q[0] = ''
        for j in s[1:]:
            q[0] += j
        print(q[0])
        print(q[-1])
        #question = Question.objects.create(text=q[0], answer=q[-1], unit=unit, source = source)

