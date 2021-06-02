import requests
from bs4 import BeautifulSoup

class Streams:
    """
    Fetch current livestreams from the VLR homepage.
    """
    def streams():
        URL = 'https://www.vlr.gg/'
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        streamLinks = soup.find_all('div', class_="js-home-streams")[0].find_all('a')
        streams = []
        for stream in streamLinks:
            title = stream['title']
            link = stream['href']
            viewers = stream.find_all('div', class_="stream-item-count")[0].get_text().strip()
            name = stream.find_all('span', class_="stream-item-txt-name")[0].get_text().strip()
            streams.append({"name" : name, "title": title, "viewers": viewers, "link": link})

        return streams