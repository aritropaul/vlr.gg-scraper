import requests
from bs4 import BeautifulSoup


class News:
    """
    Gets the news from the VLR homepage
    """

    def news():
        URL = 'https://www.vlr.gg/'
        page = requests.get(URL)

        soup = BeautifulSoup(page.content, 'html.parser')
        news = soup.find_all('div', class_="js-home-news")[0]
        dates = news.find_all('div', class_="wf-label")
        cards = news.find_all('div', class_="wf-card")
        newsDict = []
        for key in dates:
            for value in cards:
                newsLink = value.find_all('a', class_="news-item")
                for newsItem in newsLink:
                    news = {}
                    title = newsItem.find_all('div', class_="news-item-title")[0].get_text().strip()
                    link = newsItem.get('href')
                    news["date"] = key.get_text().strip().split(" \n")[0]
                    news["news"] = title
                    news["id"] = link.split("/")[1].split("/")[0]
                    newsDict.append(news)
                cards.remove(value)
                break
        return newsDict