import requests
from bs4 import BeautifulSoup
import random


class Crawler:
    # meme websites source
    websites = ["gifvif", "memedroid"]

    # Main default getter
    @staticmethod
    async def Getter():
        # initialize the meme dict
        meme = {}

        # select a random website
        site = random.choice(Crawler.websites)

        if site == "gifvif":
            meme["website"] = "gif-vif.com"
            meme["meme"] = Crawler.gifVif()
        elif site == "memedroid":
            meme["website"] = "memedroid.com"
            meme["meme"] = Crawler.memeDroid()
        elif site == "imgflip":
            meme["website"] = "imgflip.com"
            meme["meme"] = Crawler.imgFlip()

        # return the meme
        return meme

    # Specfic Website compiler
    @staticmethod
    async def Compiler(website):
        # initialize the meme dict
        meme = {}

        if website == "gifvif":
            meme["website"] = "gif-vif.com"
            meme["meme"] = Crawler.gifVif()
        elif website == "memedroid":
            meme["website"] = "memedroid.com"
            meme["meme"] = Crawler.memeDroid()
        elif website == "imgflip":
            meme["website"] = "imgflip.com"
            meme["meme"] = Crawler.imgFlip()

        return meme

    # GifVif website
    @staticmethod
    def gifVif():
        # initialize the website
        site = "https://www.gif-vif.com/category/funny/"
        page = random.randrange(376)  # generate a random page num

        # get the soup
        soup = BeautifulSoup(requests.get(site + str(page)).text, "html.parser")

        # get all of the links containers
        containers = soup.find("div", id="gif_container").find_all("a")

        # select one from the containers
        raw = random.choice(containers)

        # initialize meme dict
        meme = {}

        # get the gif src
        soup_rc = BeautifulSoup(requests.get(raw["href"]).text, "html.parser")

        # get the title
        meme["title"] = soup_rc.find("div", id="name_of_gif").get_text()

        # extact the src from the video tag
        meme["src"] = soup_rc.find("div", id="gif_div").find("source")["src"]

        # return the links
        return meme

    # MemeDroid website
    @staticmethod
    def memeDroid():
        # initialize the website
        site = "https://www.memedroid.com/memes/random"

        # get the soup
        soup = BeautifulSoup(requests.get(site).text, "html.parser")

        # find all containers
        containers = soup.find_all("div", class_="item-aux-container")

        memes = []

        for i in containers:
            raw = {}

            # get img src
            src = ""
            try:
                src = i.find("img")["src"]
            except Exception:
                pass

            if src.startswith("https://images"):
                # get the meme title
                raw["title"] = i.find("a", class_="item-header-title").get_text()
                raw["src"] = src

                # append the raw
                memes.append(raw)

        return random.choice(memes)

    # imgFlip (the api just returns template, so well just scrape the latest contents)
    @staticmethod
    def imgFlip():
        site = "https://imgflip.com/?sort=latest"
        
        # get the soup
        soup = BeautifulSoup(requests.get(site).text, 'html.parser')

        # get all containers
        containers = soup.find_all("div", class_="base-unit")

        # select a random from the containers
        con = random.choice(containers)

        # compile
        meme = {}
        meme["title"] = con.find("h2", class_="base-unit-title").get_text() # get the title
        meme["src"] = "https:" + con.find("img")["src"] # get the img src

        return meme