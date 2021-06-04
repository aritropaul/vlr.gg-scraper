from os import name
import requests
from bs4 import BeautifulSoup
from requests.api import head

class Team:
    """
    Gets all info related to teams
    """
    def team(id):
        
        URL = 'https://www.vlr.gg/team/'+id
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        header_info = {}
        roster_info = []
        transaction_info = []
        def basic_info():
            """
            Gets basic info based on the team id
            """
            header = soup.find_all('div', class_='team-header')[0]
            header_info['name'] = soup.find_all('div',class_='team-header-name')[0].find_all('h1')[0].get_text().strip()
            if len(soup.find_all('div',class_='team-header-name')[0].find_all('h2')) > 0:
                header_info['short_name'] = soup.find_all('div',class_='team-header-name')[0].find_all('h2')[0].get_text().strip()
            else:
                header_info['short_name'] = ""
            header_info['logo'] = "https:" + header.find_all('div', class_='team-header-logo')[0].find_all('img')[0]['src']
            if len(soup.find_all('div',class_='team-header-website')) > 0:
                header_info['website'] = "https://" + soup.find_all('div',class_='team-header-website')[0].find_all('a')[0].get_text().strip()
            header_info['country'] = soup.find_all('div',class_='team-header-country')[0].get_text().strip()
            if len(soup.find_all('div',class_='team-header-twitter')) > 0:
                header_info['twitter'] = soup.find_all('div',class_='team-header-twitter')[0].find_all('a')[0]['href']
            header_info['country'] = soup.find_all('div',class_='team-header-country')[0].find_all('i',class_=True)[0]['class'][1].split('-')[-1]
        
        def roster():
            """
            Gets Teaam specific roster info
            """
            roster = soup.find_all('div', class_ = 'team-roster-item')
            for roster_item in roster :
                alias_name = roster_item.find_all('div',class_='team-roster-item-name-alias')[0].get_text().strip()
                roster_player = {}
                roster_player['id'] = roster_item.find('a')['href'].split('/')[2]
                roster_player['alias_name'] = alias_name
                if len(roster_item.find_all('div',class_='team-roster-item-name-real')) > 0:
                    roster_player['real_name'] = roster_item.find_all('div',class_='team-roster-item-name-real')[0].get_text().strip()
                roster_player['country'] = roster_item.find_all('div',class_='team-roster-item-name-alias')[0].find_all('i',class_=True)[0]['class'][1].split('-')[-1]
                roster_player['is_captain'] = False
                if len(roster_item.find_all('i',class_='fa-star')) >0 :
                    roster_player['is_captain'] = True
                
                roster_player['player_pic'] = roster_item.find_all('div',class_='team-roster-item-img')[0].find_all('img')[0]['src']
                if roster_player['player_pic'] == '/img/base/ph/sil.png' :
                    roster_player['player_pic'] = 'https://www.vlr.gg'+ roster_player['player_pic']
                else:
                    roster_player['player_pic'] = 'https:'+ roster_player['player_pic']
                roster_player['player_pic'] = roster_player['player_pic']
                roster_player['player_role'] = "active"
                if len(roster_item.find_all('div',class_='team-roster-item-name-role')) > 0:
                    roster_player['player_role'] = roster_item.find_all('div',class_='team-roster-item-name-role')[0].get_text().strip()
                roster_info.append(roster_player)

        def transaction():
            """
            Gets player transactions
            """
            transaction_url = 'https://www.vlr.gg/team/transactions/' + id
            transaction_page = requests.get(transaction_url)
            bs = BeautifulSoup(transaction_page.content,'html.parser')
            for player in bs.find_all('div',class_="wf-module-item"):
                player_info = {}
                player_info['alias_name'] = player.find_all('a')[0].get_text().strip()
                player_info['id'] = player.find_all('a')[0]['href'].split('/')[2]
                player_info['country'] = player.find_all('i',class_=True)[0]['class'][1].split('-')[-1]
                player_info['transaction'] = player.find_all('div')[1].find_all('span')[0].get_text().strip()
                player_info['transaction_date'] = player.find_all('div')[2].get_text().strip().replace('\n','').replace('\t','').replace('on','').strip()
                transaction_info.append(player_info)


        basic_info()
        roster()
        transaction()
        return { "team" : id, "header" : header_info, "roster": roster_info, "transactions": transaction_info }