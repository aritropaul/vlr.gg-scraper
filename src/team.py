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
        print(URL)
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        header_info = {}
        roster_info = {}
        def basic_info():
            """
            Gets basic info based on the team id
            """
            header = soup.find_all('div', class_='team-header')[0]
            header_info['name'] = soup.find_all('div',class_='team-header-name')[0].find_all('h1')[0].get_text().strip()
            header_info['short_name'] = soup.find_all('div',class_='team-header-name')[0].find_all('h2')[0].get_text().strip()
            header_info['logo'] = header.find_all('div', class_='team-header-logo')[0].find_all('img')[0]['src'][2:]
            header_info['website'] = soup.find_all('div',class_='team-header-website')[0].find_all('a')[0].get_text().strip()
            header_info['country'] = soup.find_all('div',class_='team-header-country')[0].get_text().strip()
            header_info['twitter'] = soup.find_all('div',class_='team-header-twitter')[0].find_all('a')[0]['href']
            header_info['country'] = soup.find_all('div',class_='team-header-country')[0].find_all('i',class_=True)[0]['class'][1].split('-')[-1]
        
        def roster():
            """
            Gets Teaam specific roster info
            """
            roster = soup.find_all('div', class_ = 'team-roster-item')
            for roster_item in roster :
                alias_name = roster_item.find_all('div',class_='team-roster-item-name-alias')[0].get_text().strip()
                roster_info[alias_name]={}
                roster_info[alias_name]['alias_name'] = alias_name
                roster_info[alias_name]['real_name'] = roster_item.find_all('div',class_='team-roster-item-name-real')[0].get_text().strip()
                roster_info[alias_name]['country'] = roster_item.find_all('div',class_='team-roster-item-name-alias')[0].find_all('i',class_=True)[0]['class'][1].split('-')[-1]
                roster_info[alias_name]['is_captain'] = False
                if len(roster_item.find_all('i',class_='fa-star')) >0 :
                    roster_info[alias_name]['is_captain'] = True
                
                roster_info[alias_name]['player_pic'] = roster_item.find_all('div',class_='team-roster-item-img')[0].find_all('img')[0]['src']
                if roster_info[alias_name]['player_pic'] == '/img/base/ph/sil.png' :
                    roster_info[alias_name]['player_pic'] = '//https://www.vlr.gg'+roster_info[alias_name]['player_pic']
                roster_info[alias_name]['player_pic'] = roster_info[alias_name]['player_pic'][2:]
                
                if len(roster_item.find_all('div',class_='team-roster-item-name-role')) > 0:
                    roster_info[alias_name]['player_role'] = roster_item.find_all('div',class_='team-roster-item-name-role')[0].get_text().strip()




        basic_info()
        roster()
        return { "team" : id, "header" : header_info, "roster":roster_info}