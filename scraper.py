import requests
from bs4 import BeautifulSoup

def get_pages_from_search(ques):
    URL = 'https://www.realmeye.com/wiki-search?q=' + ques.replace(" ", "%20")
    print(URL)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    body = soup.find('body')
    pages = body.find_all('p', class_="wiki-search-result")
    outputs = []
    for page in pages:
        link = page.find('a')
        outputs.append('https://www.realmeye.com' + link['href'])
    return outputs

def get_realmeye_response(term):
    URL = 'https://www.realmeye.com/wiki/realm-eye-responses'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    body = soup.find('body')
    page_wiki = body.find('div', class_='wiki-page')
    responses = page_wiki.findChildren("p", recursive=True)

    for response in responses:
        try:
            name = response.find("a").text
            content = response.text
            if name == term:
                return content
        except:
            pass

def get_player_info(player):
    try:
        URL = 'https://www.realmeye.com/player/'+player
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
        page = requests.get(URL, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        summ = soup.find('table', class_='summary')
        info = summ.find_all('td')
        infotext = []
        for inf in info:
            infotext.append(inf.text)
        return infotext
    except:
        return None
    
def get_player_description(player):
    try:
        URL = 'https://www.realmeye.com/player/'+player
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
        page = requests.get(URL, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        desc = soup.find('div', class_='line1 description-line')
        infotext = desc.text
        return infotext
    except:
        return None

def get_wiki_page(url_):
    finalout = []
    URL = url_
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    body = soup.find('body')
    main = body.find('div', class_='table-responsive')
    name = main.find('img')['title']
    page_wiki = body.find('div', class_='wiki-page')
    children = page_wiki.findChildren("div", class_="table-responsive", recursive=False)
    first = children[0]
    tds = first.find_all('td')
    description = tds[1].text

    
    #checking if has reskin
    child2 = children[1]
    child3 = child2.find('th')
    if (child3.text) == 'Reskin(s)':
        stats = children[2].find_all('tr')
        notes = page_wiki.findChildren("p", recursive=False)
    else:
        stats = children[1].find_all('tr')
        notes = page_wiki.findChildren("p", recursive=False)
    notemessage = ''
    for note in notes:
        notemessage += note.text + '\n'

    tier_ = stats[0]
    tier_step = (tier_.find_all('th'))
    statlist = []
    tier = (tier_step[0].text + ': ' + tier_step[1].text)
    statlist.append(tier)
    stats.pop(0)
    for stat in stats:
        part1 = stat.find('th').text
        part2 = stat.find('td').text
        if part1 == 'Soulbound':
            combined = part1
        else:
            combined = part1 + ': ' + part2
        statlist.append(combined)
    finalout.append(name)
    finalout.append(statlist)
    finalout.append(description)
    finalout.append(notemessage)
    return finalout

