# <-- Imports -->
import grequests
import asyncio
import json
import os
import discord
import datetime
from discord.ext import tasks, commands
from utils.api import Cat
from utils.logger import Logger

# <-- Classes -->
class Bot(commands.Bot):
    def __init__(self):
        super().__init__(intents=discord.Intents.default(), command_prefix="")

    async def setup_hook(self):
        log.info('Loading commands...')
        for file in os.listdir('commands'):
            if file.endswith('.py'):
                await self.load_extension(f'commands.{os.path.splitext(file)[0]}')
        log.success('Finished loading commands!')

    async def on_ready(self):
        await self.wait_until_ready()
        log.info('Syncing slash commands...')
        await bot.tree.sync()
        log.success('Finished syncing slash commands!')

        log.success(f'Successfully logged in as {self.user}')

        # hourlyPhotoStarter.start()
        # scrapeVideos.start()
        # rpc.start()

# <-- Tasks -->
# Task to change the presence of the bot every minute to the current server count
@tasks.loop(minutes=1)
async def rpc():
    activity = discord.Activity(type=discord.ActivityType.listening, name=f"/help in {len(bot.guilds)} servers")
    await bot.change_presence(activity=activity)

# Task to scrape videos from a variety of different subreddits
@tasks.loop(hours=1)
async def scrapeVideos():
    log.info('Scraping videos from Reddit.')

    rs = (grequests.get(f'https://www.reddit.com/r/{u}.json?sort=hot&t=day&limit=100', headers=headers) for u in cat.subList)
    responses = grequests.map(rs)

    try:
        with open('data.json', 'r', encoding='utf8') as f:
            data = json.load(f)
            data['videos'] = []
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        data = {
            'webhooks': {},
            'videos': []
        }

    for index, response in enumerate(responses):
        try:
            subData = response.json()['data']['children']

            for item in subData:
                obj = item['data']

                if not obj['is_video']:
                    continue

                # Parse only the data that I need, and add it to the videos array in data.json
                data['videos'].append(
                    {
                        'title': obj['title'].encode().decode('utf8'),
                        'author': obj['author'],
                        'subreddit': obj['subreddit'],
                        'permalink': f'https://www.reddit.com{obj["permalink"]}',
                        'video': obj['secure_media']['reddit_video']['fallback_url'].split('?')[0]
                    }
                )

        except Exception:
            log.error(f"Error scraping videos from r/{cat.subList[index]}.")

    with open('data.json', 'w', encoding='utf8') as f:
        f.write(json.dumps(data))

    log.success('Finished scraping videos from Reddit!')

# Hourly cat photo using the /schedule command
# I need to use a separate task for this because I can't mix relative time and explicit time
# Discord.py moment
# @tasks.loop(time=datetime.time(hour=datetime.datetime.now().hour + 1, minute=0))
# async def hourlyPhotoStarter():
#     hourlyPhoto.start()

@tasks.loop(hours=1)
async def hourlyPhoto():
    log.info('Sending photos to webhooks.')

    with open('data.json', 'r', encoding='utf8') as f:
        data = json.load(f)

    pfp = bot.user.display_avatar
    img_obj = await cat.image()
    img = img_obj[0]['url']

    for index in dict(data['webhooks']):
        url = data['webhooks'][index]
        postData = {
            "username": "Cat Bot",
            "avatar_url": pfp,
            "embeds": [
                {
                    "title": "Hourly Cat Photo",
                    "color": 0x3498DB,
                    "image": {
                        "url": img
                    }
                }
            ]
        }

        result = await cat.make_request('POST', url, json=postData)

        if result.status_code == 404:
            log.error('Error sending hourly photo: Webhook not found.')
            log.info('Removing webhook from schedule.')
            data['webhooks'].pop(index)
        elif result.status_code == 429:
            log.error('Error sending hourly photo: Rate limited.')
            log.info('Retrying in 10 seconds.')
            await asyncio.sleep(10)

            await cat.make_request('POST', url, json=postData)

        await asyncio.sleep(2.5)

    with open('data.json', 'w', encoding='utf8') as f:
        f.write(json.dumps(data))

    log.success('Finished sending photos to webhooks.')

# <-- Variables -->
bot = Bot()
cat = Cat()
log = Logger()
headers = {
    'User-Agent': 'Cat Bot - https://github.com/paintingofblue/thecatapi-discord-bot'
}

try:
    log.info('Logging in to Discord...')
    bot.run(cat.token)
except Exception as e:
    log.error(f'An error has occurred when logging into Discord: {e}')