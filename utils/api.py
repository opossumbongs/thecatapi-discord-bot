import aiohttp
import random
from bs4 import BeautifulSoup
from typing import Optional, Union

class Cat():
    def __init__(self):
        self.embedColor = 0x3498DB
        self.baseURL = 'https://api.thecatapi.com/v1/'
        self.subList = ['IllegallySmolCats', 'cats', 'Catloaf', 'Catswithjobs', 'WhatsWrongWithYourCat', 'blackcats', 'CatSlaps', 'SupermodelCats', 'CatsStandingUp', 'bigcatgifs', 'catbellies', 'catpictures', 'catpranks', 'catsareliquid', 'catsinsinks', 'catsinbusinessattire', 'catswhoyell', 'catswithjobs', 'cattaps', 'catsisuottafo', 'blep', 'fromkittentocat', 'holdmycatnip', 'jellybeantoes', 'kittens', 'kitting', 'kneadycats', 'mainecoons', 'murdermittens', 'nebelung', 'petthedamncat', 'pocketpussy', 'ragdolls', 'startledcats', 'stuffoncats', 'teefies', 'thecattrapisworking', 'tightpussy', 'toebeans', 'tuckedinkitties']
        self.keyList = ['']
        self.token = ''

    async def make_request(self, url: str, method: str='GET', headers: dict = {}, data: dict = {}, json: dict = {}) -> aiohttp.ClientResponse:
        headers['User-Agent'] = 'Cat Bot - https://github.com/paintingofblue/thecatapi-discord-bot'

        if not url.startswith('https://'):
            url = f'{self.baseURL}{url}'

        session = aiohttp.ClientSession()
        if method == 'POST':
            response = await session.request(method, url, headers=headers, data=data, json=json)
        else:
            response = await session.request(method, url, headers=headers)
        await session.close()
        return response

    async def get(self, url: str, headers: dict = {}):
        response = await self.make_request(url, headers=headers)
        return response


    # Fetching image
    async def image(self, *, breed: Optional[str] = None, amount: Optional[int] = 1):
        if breed:
            response = await self.make_request(f'images/search?mime_types=jpg,png&breed_ids={breed}&limit={amount}', headers={'x-api-key': random.choice(self.keyList)})
            return await response.json()
        else:
            response = await self.make_request(f'images/search?mime_types=jpg,png&limit={amount}', headers={'x-api-key': random.choice(self.keyList)})
            return await response.json()

    # Fetching gif
    async def gif(self):
        if random.randint(1, 2) == 1:
            response = await self.make_request('images/search?mime_types=gif', headers={'x-api-key': random.choice(self.keyList)})
            return await response.json()
        else:
            response = await self.make_request('https://edgecats.net/all')
            soup = BeautifulSoup(response.text, features='html.parser')
            gifLinks = soup.findAll('a', href=True)
            return random.choice(gifLinks).get('href')

    # Fetching a video (this is used in tandem with cobalt and reddit)
    async def video(self, url: str) -> str:
        # use cobalt's api by wukko
        # need to do some logic for passing in the post url & then fetch the video with audio from cobalt
        pass

    # Fetching fact
    async def facts(self) -> list:
        response = await self.make_request('https://gist.githubusercontent.com/paintingofblue/657d0c4d1202374889ce4a98a6b7f35f/raw/catfacts.txt')
        facts = response.text.splitlines()
        return facts

    # Fetching breeds
    async def get_breeds(self):
        response = await self.make_request('breeds', headers={'x-api-key': random.choice(self.keyList)})
        return await response.json()

    # Fetching info about a specific breed
    async def get_breed_info(self, breedid: Union[int, str]):
        response = await self.make_request(f'breeds/{breedid}', headers={'x-api-key': random.choice(self.keyList)})
        return await response.json()
