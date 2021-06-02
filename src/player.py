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
        if len(container1.find_all('div', class_="wf-card")) > 2:
            currentTeamCard = container1.find_all('div', class_="wf-card")[2].find('a')
            teamIcon = "https:" + currentTeamCard.find('img')['src']
            teamName = currentTeamCard.find_all('div')[1].find('div').get_text().strip()
            desc = currentTeamCard.find_all('div')[1].find_all('div')[2].get_text().strip()
        else:
            teamIcon = ""
            teamName = ""
            desc = ""

        recentMatches = []
        matches = container1.find_all('div', class_="wf-card")[1].find_all('a')
        for match in matches:
            stage = match.find_all('div', class_="rm-item-event")[0].find_all('div', class_="text-of")[0].get_text().strip()
            event = match.find_all('div', class_="rm-item-event")[0].find_all('div', class_="text-of")[1].get_text().strip()
            score = match.find_all('span', class_="rf")[0].get_text().strip() + "-" + match.find_all('span', class_="ra")[0].get_text().strip()
            if match.find_all('div', class_="rm-item-opponent")[0].find('img') != None:
                opponentIcon = "https:" + match.find_all('div', class_="rm-item-opponent")[0].find('img')['src']
            else :
                opponentIcon = ""
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
        events = container2.find_all('div',class_="wf-card")[-1].find_all('a')
        total = container2.find_all('div',class_="wf-card")[-1].find('div').find('span').get_text().strip()
        for place in events:
            eventName = place.find_all('div', class_="text-of")[0].get_text().strip()
            podium = place.find('div').find_all('div')[1].find_all('span')[0].get_text().strip().replace('\t', '').replace('\n', ' ')
            spanNodes = place.find('div').find_all('div')[1].find_all('span')
            prize = ""
            if len(spanNodes) > 1:
                prize = place.find('div').find_all('div')[1].find_all('span')[1].get_text().strip()
            eventPlacement.append( { 'name': eventName, 'position': podium, 'prize': prize } )

        stats = []
        if len(soup.find_all('table', class_="wf-table")) > 0:
            statRows = soup.find_all('table', class_="wf-table")[0].find('tbody').find_all('tr')
            for row in statRows:
                agent = "https://vlr.gg" + row.find_all('td')[0].find('img')['src']
                pick = row.find_all('td')[1].get_text().strip()
                rounds = row.find_all('td')[2].get_text().strip()
                acs = row.find_all('td')[3].get_text().strip()
                kd = row.find_all('td')[4].get_text().strip()
                adr = row.find_all('td')[5].get_text().strip()
                kpr = row.find_all('td')[6].get_text().strip()
                apr = row.find_all('td')[7].get_text().strip()
                fkpr = row.find_all('td')[8].get_text().strip()
                fdpr = row.find_all('td')[9].get_text().strip()
                k = row.find_all('td')[10].get_text().strip()
                d = row.find_all('td')[11].get_text().strip()
                a = row.find_all('td')[12].get_text().strip()
                fk = row.find_all('td')[13].get_text().strip()
                fd = row.find_all('td')[14].get_text().strip()
                stat = { 'agent': agent, 'pick': pick, 'rounds': rounds, 'acs': acs, 'kd': kd, 'adr': adr, 'kpr': kpr, 'apr':apr, 'fkpr': fkpr, 'fdpr': fdpr, 'kills':k, 'deaths': d, 'assists': a, 'fk': fk, 'fd': fd}
                stats.append(stat)


        return {
                "id": id, 
                "name" : name, 
                "real_name" : real_name,
                "twitter": twitterHandle, 
                "twitch": twitchHandle,
                "country" : country,
                "team": { 'name': teamName, 'icon': teamIcon, 'desc': desc},
                "past_teams" : pastTeams,
                "recent" : recentMatches,
                "stats": stats,
                "placement": { 'total' : total, 'events': eventPlacement }
        }