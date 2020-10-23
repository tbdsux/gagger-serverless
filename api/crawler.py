import requests
from bs4 import BeautifulSoup
import random

class Crawler:
    # meme websites source
    websites = ['gifvif', 'memedroid']

    # Main default getter
    @staticmethod
    async def Getter():
        # initialize the meme dict
        meme = {}

        # select a random website
        site = random.choice(Crawler.websites)

        if site == 'gifvif':
            meme["website"] = "gif-vif.com"
            meme["meme"] = Crawler.gifVif()
        elif site == 'memedroid':
            meme["website"] = "memedroid.com"
            meme["meme"] = Crawler.memeDroid()

        # return the meme
        return meme

    # Specfic Website compiler
    @staticmethod
    async def Compiler(website):
        # initialize the meme dict
        meme = {}

        if website == 'gifvif':
            meme["website"] = "gif-vif.com"
            meme["meme"] = Crawler.gifVif()
        elif website == 'memedroid':
            meme["website"] = "memedroid.com"
            meme["meme"] = Crawler.memeDroid()

        return meme

    # GifVif website
    @staticmethod
    def gifVif():
        # initialize the website
        site = "https://www.gif-vif.com/category/funny/"
        page = random.randrange(376) # generate a random page num

        # get the soup
        soup = BeautifulSoup(requests.get(site + str(page)).text, 'html.parser')
        
        # storage for all memes found
        links = []

        # get all of the links containers
        containers = soup.find("div", id="gif_container").find_all("a")

        for i in containers:
            raw = {}

            # get the title
            raw['title'] = i.find("div", class_="gif_title_gl").get_text()

            # get the gif src
            soup_rc = BeautifulSoup(requests.get(i["href"]).text, 'html.parser')
            
            # extact the src from the video tag
            raw['src'] = soup_rc.find("div", id="gif_div").find("source")["src"]

            # append the raw
            links.append(raw)

        # return the links
        return random.choice(links)

    # MemeDroid website
    @staticmethod
    def memeDroid():
        # initialize the website
        site = "https://www.memedroid.com/memes/random"

        # get the soup
        soup = BeautifulSoup(requests.get(site).text, 'html.parser')

        # find all containers
        containers = soup.find_all("div", class_="item-aux-container")

        memes = []

        for i in containers:
            raw = {}

            # get img src
            src = ''
            try:
                src = i.find("img")["src"]
            except Exception:
                pass

            if src.startswith('https://images'):
                # get the meme title
                raw['title'] = i.find("a", class_="item-header-title").get_text()
                raw["src"] = src

                # append the raw
                memes.append(raw)

        return random.choice(memes)