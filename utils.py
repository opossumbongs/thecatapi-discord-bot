import requests
import random
from bs4 import BeautifulSoup
from datetime import datetime

# API wrapper for https://thecatapi.com
class Cat():
    def __init__(self):
        self.embedColor = 0x3498DB
        self.subList = ['IllegallySmolCats', 'cats', 'Catloaf', 'Catswithjobs', 'WhatsWrongWithYourCat', 'blackcats', 'CatSlaps', 'SupermodelCats', 'CatsStandingUp', 'bigcatgifs', 'catbellies', 'catpictures', 'catpranks', 'catsareliquid', 'catsinsinks', 'catsinbusinessattire', 'catswhoyell', 'catswithjobs', 'cattaps', 'catsisuottafo', 'blep', 'fromkittentocat', 'holdmycatnip', 'jellybeantoes', 'kittens', 'kitting', 'kneadycats', 'mainecoons', 'murdermittens', 'nebelung', 'petthedamncat', 'pocketpussy', 'ragdolls', 'startledcats', 'stuffoncats', 'teefies', 'thecattrapisworking', 'tightpussy', 'toebeans', 'tuckedinkitties']
        self.keyList = ['enter-keys-here']
        self.token = 'enter-token-here'

    # Fetching image
    def image(self, *, breed):
        if breed:
            r = requests.get(f'https://api.thecatapi.com/v1/images/search?mime_types=jpg,png&breed_ids={breed}', headers={'x-api-key': random.choice(self.keyList)})
            return r.json()
        else:
            r = requests.get('https://api.thecatapi.com/v1/images/search?mime_types=jpg,png', headers={'x-api-key': random.choice(self.keyList)})
            return r.json()

    # Fetching gif
    def gif(self):
        if random.randint(1, 2) == 1:
            r = requests.get('https://api.thecatapi.com/v1/images/search?mime_types=gif', headers={'x-api-key': random.choice(self.keyList)})
            return r.json()
        else:
            r = requests.get('https://edgecats.net/all')
            soup = BeautifulSoup(r.text)
            gifLinks = soup.findAll('a', href=True)
            return random.choice(gifLinks).get('href')

    # Fetching fact
    def fact(self):
        r = requests.get('https://gist.githubusercontent.com/paintingofblue/657d0c4d1202374889ce4a98a6b7f35f/raw/catfacts.txt')
        return random.choice(r.text.splitlines())

    # Fetching breeds
    def get_breeds(self):
        r = requests.get('https://api.thecatapi.com/v1/breeds', headers={'x-api-key': random.choice(self.keyList)})
        return r.json()

    # Fetching info about a specific breed
    def get_breed_info(self, breedid):
        r = requests.get(f'https://api.thecatapi.com/v1/breeds/{breedid}', headers={'x-api-key': random.choice(self.keyList)})
        return r.json()

# Logger
class Logger:
    # Initialize colors using ANSI escape codes
    def __init__(self):
        self.red = '\033[91m'
        self.yellow = '\033[93m'
        self.green = '\033[92m'
        self.grey = '\033[90m'
        self.reset = '\033[37m'

    def info(self, text):
        time = datetime.now().strftime("%D %H:%M:%S")
        print(f'{self.grey}[+]{self.reset} {time} - {text}')

    def error(self, text):
        time = datetime.now().strftime("%D %H:%M:%S")
        print(f'{self.red}[-]{self.reset} {time} - {text}')

    def warning(self, text):
        time = datetime.now().strftime("%D %H:%M:%S")
        print(f'{self.yellow}[!]{self.reset} {time} - {text}')

    def success(self, text):
        time = datetime.now().strftime("%D %H:%M:%S")
        print(f'{self.green}[+]{self.reset} {time} - {text}')