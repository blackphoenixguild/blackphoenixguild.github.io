import requests
from bs4 import BeautifulSoup

URL = 'https://www.realmeye.com/guild/BlackPhoenix'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
page = requests.get(URL, headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')
body = soup.find('body')
pages = body.find('table', class_="table table-striped tablesorter")
rows = pages.find_all('tr')[1:]
members = []
for row in rows:
    toadd = []
    items = row.find_all('td')
    for item in items:
        toadd.append(item.text)
    members.append(toadd)
print(members)
global tablegen
tablegen = '<table style="width:100%">'

def add(text):
    global tablegen
    tablegen += text
    tablegen += '\n'

add('\n   <tr>')
add('      <th>Username</th>')
add('      <th>Rank</th>')
add('      <th>Fame</th>')
add('      <th>EXP</th>')
add('      <th>Star count</th>')
add('      <th>Characters</th>')
add('      <th>Last seen</th>')
add('      <th>Server</th>')
add('      <th>Fame / Char</th>')
add('      <th>EXP / Char</th>')
add('   </tr>')
for member in members:
    add('   <tr>')
    for thing in member:
        add('      <th>'+str(thing)+'</th>')
    add('   </tr>')
add('</table>')
print(tablegen)
