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
        
        
        basic_info()
        
        return { "team" : id, "header" : header_info}