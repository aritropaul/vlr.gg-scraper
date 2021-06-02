import requests
from bs4 import BeautifulSoup

class Events:
    """
    Get events from the VLR events page
    """

    def events(self, region):
        URL = "https://www.vlr.gg/events/" + region
        page = requests.get(URL)

        soup = BeautifulSoup(page.content, 'html.parser')
        return URL

    def region(self, id):
        if id == "all":
            return self.events("")
        elif id == "NA":
            return self.events("north-america")
        elif id == "EU":
            return self.events("europe")
        elif id == "SEA":
            return self.events("asia-pacific")
        elif id == "LATAM":
            return self.events("latin-america")
        elif id == "MENA":
            return self.events("mena")
        else:
            print("unknown")
