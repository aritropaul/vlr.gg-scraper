import requests
from bs4 import BeautifulSoup

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
                news["date"] = key.get_text().strip()
                news["news"] = title
                news["id"] = link.split("/")[1].split("/")[0]
                newsDict.append(news)
            cards.remove(value)
            break
    return newsDict


def article(id):
    URL = 'https://www.vlr.gg/' + id
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')
    title = soup.find('h1', class_='wf-title').get_text().strip()
    meta = soup.find('a', class_='article-meta-author').get_text().strip()
    date = soup.find('span', class_='js-date-toggle').get_text().strip()
    article = soup.find('div', class_='article-body')
    tweet_link = []
    articleStr = ""
    for match in article.findAll('span', class_='wf-hover-card'):
        match.replace_with('')
    for match in article.findAll('style'):
        match.replace_with('')
    for match in article.findAll('span'):
        match.replace_with(match.get_text().strip().replace('\n', '').replace('\t', ''))
    for tweet in article.findAll('div', class_='tweet'):
        tweet_link.append(tweet['data-url'])
        tweet.replace_with('')
    subline = soup.find('p').get_text().strip().replace('\n', '').replace('\t', '')
    return { 'title' : title,
             'meta': meta,
             'date': date,
             'subline': subline,
             'tweets': tweet_link,
             'content': article.get_text().strip()
            }

print(article("17201"))