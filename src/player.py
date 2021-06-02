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

        recentMatches = []
        matches = container1.find_all('div', class_="wf-card")[1].find_all('a')
        for match in matches:
            stage = match.find_all('div', class_="rm-item-event")[0].find_all('div', class_="text-of")[0].get_text().strip()
            event = match.find_all('div', class_="rm-item-event")[0].find_all('div', class_="text-of")[1].get_text().strip()
            score = match.find_all('span', class_="rf")[0].get_text().strip() + "-" + match.find_all('span', class_="ra")[0].get_text().strip()
            opponentIcon = "https:" + match.find_all('div', class_="rm-item-opponent")[0].find('img')['src']
            opponent = match.find_all('div', class_="rm-item-opponent")[0].find_all('div', class_="text-of")[0].get_text().strip()
            date = match.find_all('div', class_="rm-item-date")[0].get_text().strip().replace('\t', '').replace('\n', ' - ')
            match = {'stage' : stage,
                    'event': event,
                    'score': score,
                    'opponent' : {'img': opponentIcon, 'name': opponent},
                    'date': date
                    }
            recentMatches.append(match)

        pastTeams = []
        print(len(container1.find_all('div', class_="wf-card")))
        if len(container1.find_all('div', class_="wf-card")) > 3:
            teams = container1.find_all('div', class_="wf-card")[3].find_all('a')
            for team in teams:
                oldTeamIcon = "https:" + team.find('img')['src']
                oldTeamName = team.find_all('div')[1].find('div').get_text().strip()
                oldTeamDesc = team.find_all('div')[1].find_all('div')[2].get_text().strip()
                oldTeam = { 'name': oldTeamName, 'icon': oldTeamIcon, 'desc': oldTeamDesc }
                pastTeams.append(oldTeam)

        eventPlacement = []
        container2 = soup.find_all('div', class_="player-summary-container-2")[0]
        events = container2.find_all('div',class_="wf-card")[1].find_all('a')
        total = container2.find_all('div',class_="wf-card")[1].find('div').find('span').get_text().strip()
        for place in events:
            eventName = place.find_all('div', class_="text-of")[0].get_text().strip()
            podium = place.find('div').find_all('div')[1].find_all('span')[0].get_text().strip().replace('\t', '').replace('\n', ' ')
            spanNodes = place.find('div').find_all('div')[1].find_all('span')
            prize = ""
            if len(spanNodes) > 1:
                prize = place.find('div').find_all('div')[1].find_all('span')[1].get_text().strip()
            eventPlacement.append( { 'name': eventName, 'position': podium, 'prize': prize } )

        return { "name" : name, 
                "real_name" : real_name,
                "twitter": twitterHandle, 
                "twitch": twitchHandle,
                "country" : country,
                "team": { 'name': teamName, 'icon': teamIcon, 'desc': desc},
                "past_teams" : pastTeams,
                "recent" : recentMatches,
                "placement": { 'total' : total, 'events': eventPlacement }
        }