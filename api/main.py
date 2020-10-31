from fastapi import FastAPI

# import the crawler
from .crawler import Crawler

app = FastAPI(redoc_url=None, docs_url=None)

@app.get('/')
async def index():
    meme = await Crawler.Getter()
    return meme

@app.get('/spec/{website}')
async def spec(website: str):
    meme = await Crawler.Compiler(website)
    return meme

@app.get('/about')
async def about():
    return {
        "about": "just a simple meme scraper api"
    }