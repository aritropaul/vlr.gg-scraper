import requests
from bs4 import BeautifulSoup

class Player:
    """
    Gets player information from their vlr page
    """

    def player(id):
        return { "player" : id }