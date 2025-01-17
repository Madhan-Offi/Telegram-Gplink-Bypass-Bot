from pyrogram import Client, filters
from pyrogram.types import *
import time
import requests
import cloudscraper
from bs4 import BeautifulSoup
from urllib.parse import urlparse

API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")



bot = Client(
    "AnimeNews" ,
    api_id = API_ID ,
    api_hash = API_HASH ,
    bot_token = BOT_TOKEN
)


def gp(url):
    scraper = cloudscraper.create_scraper(allow_brotli=False)
    src = scraper.get(url)
    header = { "referer": src.url }
    src = scraper.get(url, headers=header)
    
    bs4 = BeautifulSoup(src.content, 'lxml')
    inputs = bs4.find_all('input')
    data = { input.get('name'): input.get('value') for input in inputs }

    header = {
        'content-type': 'application/x-www-form-urlencoded',
        'x-requested-with': 'XMLHttpRequest'
    }
    
    time.sleep(10) 
    
    k = urlparse(url)
    URL = f'{k.scheme}://{k.netloc}/links/go'
    src = scraper.post(URL, data=data, headers=header).json()

    return src


@bot.on_message(
    filters.command("gp", prefixes=["/", ".", "?", "-"])
    & ~filters.private)
async def gplink(_, message): 

    link = message.command[1]

    gpLink = gp(url=link)
    
    await message.reply_text(f"{gpLink}")


def droplink_bypass(url):
    client = requests.Session()
    res = client.get(url)

    ref = re.findall("action[ ]{0,}=[ ]{0,}['|\"](.*?)['|\"]", res.text)[0]

    h = {'referer': ref}
    res = client.get(url, headers=h)

    bs4 = BeautifulSoup(res.content, 'lxml')
    inputs = bs4.find_all('input')
    data = { input.get('name'): input.get('value') for input in inputs }

    h = {
        'content-type': 'application/x-www-form-urlencoded',                        
        'x-requested-with': 'XMLHttpRequest'
    }
    p = urlparse(url)
    final_url = f'{p.scheme}://{p.netloc}/links/go'

    time.sleep(3.1)
    res = client.post(final_url, data=data, headers=h).json()

    return res


@bot.on_message(
    filters.command("droplink", prefixes=["/", ".", "?", "-"])
    & ~filters.private)
async def droplink(_, message): 

    link = message.command[1]

    dropLink = drop(url=link)
    
    await message.reply_text(f"{dropLink}")


bot.run()
 

