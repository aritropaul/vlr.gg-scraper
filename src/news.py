import requests
from bs4 import BeautifulSoup


class News:
    """
    Gets the news from the VLR homepage
    """

    def news():
        URL = 'https://www.vlr.gg/news'
        page = requests.get(URL)

        soup = BeautifulSoup(page.content, 'html.parser')
        vlr_module = soup.find(id="wrapper").parent.find_all(
            "a", class_="wf-module-item"
        )

        result = []
        for module in vlr_module:

            # Titles of articles
            title = module.find(
                "div",
                attrs={"style": "font-weight: 700; font-size: 15px; line-height: 1.3;"},
            ).text.strip()

            # get descriptions of articles
            desc = module.find(
                "div",
                attrs={
                    "style": " font-size: 13px; padding: 5px 0; padding-bottom: 6px; line-height: 1.4;"
                },
            ).text.strip()

            # get date of articles
            date = module.find("div", class_="ge-text-light").get_text().strip()
            date = date.replace("\u2022", "").strip()
            date = date.strip().split("  ")[0]
            # date = datetime.strptime(date, "%b %d, %Y")
            # date = date.replace(tzinfo=date.tzinfo)
            # date = date.isoformat()

            # get author of articles
            author = module.find("div", class_="ge-text-light").get_text().strip()
            author = author.replace("\u2022", "").strip()
            author = author.strip().split("  ")[1]
            # remove "by" in author section
            author = author.strip().split(" ")[1]

            # get url_path of articles
            url = module["href"]
            result.append(
                {
                    "title": title,
                    "description": desc,
                    "date": date,
                    "author": author,
                    "link": url,
                }
            )
        return result