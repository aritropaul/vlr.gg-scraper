import requests
from bs4 import BeautifulSoup

class Rankings:
    """
    Get rankings for teams
    """

    def worldRanking(self):
        URL = 'https://www.vlr.gg/rankings'
        page = requests.get(URL)

        soup = BeautifulSoup(page.content, 'html.parser')

        ranking = []
        regions = soup.find_all('div', class_='world-rankings-col')
        for region in regions:
            name = region.find('h2', class_='wf-label mod-large mod-world').get_text().strip()
            teamsHTML = region.find_all('tr', class_="wf-card")
            teams = []
            for team in teamsHTML:
                id = team.find_all('td')[1].find('a')['href'].split('/')[2]
                rank = team.find_all('td')[0].get_text().strip()
                teamName = team.find_all('td')[1].get_text().strip().split('\t')[0]
                country = team.find_all('td')[1].find_all('div', class_="rank-item-team-country")[0].get_text().strip()
                img = team.find_all('td')[1].find('img')['src']
                if img == '/img/vlr/tmp/vlr.png':
                    img = "https://vlr.gg" + img
                else:
                    img = "https:" + img
                rating = team.find_all('td')[2].get_text().strip().split('\t')[0]
                if team.find_all('td')[2].find('i',class_="fa") != None:
                    change = team.find_all('td')[2].find('i',class_="fa").get('class')[1].split('-')[-1]
                else:
                    change = "no change"
                teams.append({'id': id, 'name': teamName, 'country':country, 'rank':rank, 'img': img, 'rating': rating, 'change': change})
            ranking.append({'region':name, 'rankings': teams})
        return ranking

    def regionRankings(self,region):
        URL = 'https://www.vlr.gg/rankings/' + region
        page = requests.get(URL)

        soup = BeautifulSoup(page.content, 'html.parser')
        table = soup.find_all('table', class_="wf-faux-table")[0]
        teams = []
        rows = table.find_all('tr', class_="wf-card")
        for row in rows:
            rank = row.find_all('td')[0].get_text().strip()
            teamName = row.find_all('td')[1].get_text().strip().split('\t')[0]
            teamID = row.find_all('td')[1].find('a')['href'].split('/')[2]
            country = row.find_all('td')[1].find_all('div', class_="rank-item-team-country")[0].get_text().strip()
            img = row.find_all('td')[1].find('img')['src']
            if img == '/img/vlr/tmp/vlr.png':
                img = "https://vlr.gg" + img
            else:
                img = "https:" + img
            rating = row.find_all('td')[2].get_text().strip().split('\t')[0]
            if row.find_all('td')[2].find('i',class_="fa") != None:
                change = row.find_all('td')[2].find('i',class_="fa").get('class')[1].split('-')[-1]
            else:
                change = "no change"
            last_played = row.find_all('td')[3].get_text().strip().replace('\t','').replace('\n',' ').replace('  ', ' ')
            last_playedID = row.find_all('td')[3].find('a')['href'].split('/')[1]
            streak = row.find_all('td')[4].get_text().strip()
            record = row.find_all('td')[5].get_text().strip()
            winnings = row.find_all('td')[6].get_text().strip()
            teams.append({'id': teamID, 'name': teamName, 'country':country, 'rank':rank, 'img': img, 'rating': rating,  'change': change, 'streak': streak, 'last_played': last_played, 'last_played_ID': last_playedID, 'record': record, 'winnings': winnings})
        return teams

    def regions(self):
        URL = 'https://www.vlr.gg/rankings/'
        page = requests.get(URL)

        soup = BeautifulSoup(page.content, 'html.parser')
        nav = soup.find_all('div', class_='wf-nav')[0]
        regions = []
        links = nav.find_all('a')
        for link in links:
            region = {}
            region['link'] = link['href']
            region['region'] = link.find('span', class_='normal').get_text().strip()
            regions.append(region)
        
        return regions