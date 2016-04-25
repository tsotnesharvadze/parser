import urllib.request
from htmldom import htmldom

class LinkGetter:
    @staticmethod
    def get_links(page=1):
        data = urllib.request.urlopen("http://receptebi.ge/page/" + str(page)).read().decode()
        dom = htmldom.HtmlDom().createDom(data)
        links = []
        divs = dom.find("div[class=loop-entry-thumbnail]")

        if divs is None:
            return []

        for div in dom.find("div[class=loop-entry-thumbnail]"):
            links.append(div.find("a").first().attr("href"))

        return links
