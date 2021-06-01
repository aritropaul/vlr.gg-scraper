import requests
from bs4 import BeautifulSoup
from requests.api import head

class Player:
    """
    Gets player information from their vlr page
    """

    def player(id):
        URL = 'https://www.vlr.gg/player/' + id
        page = requests.get(URL)

        soup = BeautifulSoup(page.content, 'html.parser')
        header = soup.find_all('div', class_="player-header")[0]
        name = header.find_all('h1', class_="wf-title")[0].get_text().strip()
        real_name = soup.find_all('h2', class_="player-real-name")[0].get_text().strip()
        if len(header.find_all('a')) > 1:
            twitterHandle = header.find_all('a')[0]['href']
            twitchHandle = header.find_all('a')[1]['href']
        else:
            twitterHandle = ""
            twitchHandle = ""

        country = header.find_all('i', class_="flag")[0].get('class')[1].replace('mod-', '')
        container1 = soup.find_all('div', class_="player-summary-container-1")[0]
        currentTeamCard = container1.find_all('div', class_="wf-card")[2].find('a')
        teamIcon = "https:" + currentTeamCard.find('img')['src']
        teamName = currentTeamCard.find_all('div')[1].find('div').get_text().strip()
        desc = currentTeamCard.find_all('div')[1].find_all('div')[2].get_text().strip()
        return { "name" : name, 
                "real_name" : real_name, 
                "twitter": twitterHandle, 
                "twitch": twitchHandle,
                "country" : country,
                "team": { 'name': teamName, 'icon': teamIcon, 'desc': desc}
        }