import urllib.request
from html.parser import HTMLParser
from htmldom import htmldom
import re

class Parser:
    vowels = {
        "ა": True,
        "ე": True,
        "ი": True,
        "ო": True,
        "უ": True
    }

    @staticmethod
    def get_data(link):
        try:
            data = urllib.request.urlopen(link).read().decode()
            dom = htmldom.HtmlDom().createDom(data)
            image = dom.find("img.attachment-post-full").first().attr("src")
            title = dom.find("h1#title").first().text()
            ul = dom.find("div.entry ul").first()
            rules = []
            ingredients = []
            recipe_paragraphs = ul.next("p").first().nextUntil("div")
            recipe = ""
            regex = re.compile("[\xa0\s]+")

            for p in recipe_paragraphs:
                recipe += p.html()

            for li in ul.find("li"):
                rule = li.text()
                rules.append(rule)
                p = regex.split(rule.strip())
                l = len(p)
                i = l - 1
                r = p[i]
                ch = r[-1:]

                while ch is not None and not (r[-1:] in Parser.vowels):
                    i -= 1
                    if i >= 0 and i < l:
                        r = p[i]
                        ch = r[-1:]
                    else:
                        r = None
                        break

                if r is None:
                    continue

                if i < (l - 1) and p[i - 1][-2:] == "ის":
                    r = p[i - 1] + " " + r

                ingredients.append(r)

            return {
                "image": image,
                "title": title,
                "rules": rules,
                "recipe": recipe,
                "ingredients": ingredients,
                "source": link
            }
        except:
            print("Failed to request resource: ", link)
            return None
