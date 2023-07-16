import os
import requests
import random
import json
from pathlib import Path
from bs4 import BeautifulSoup
from datetime import datetime
from typing import Optional, Union

# API wrapper for https://thecatapi.com
class Cat():
    def __init__(self):
        self.embedColor = 0x3498DB
        self.subList = ['IllegallySmolCats', 'cats', 'Catloaf', 'Catswithjobs', 'WhatsWrongWithYourCat', 'blackcats', 'CatSlaps', 'SupermodelCats', 'CatsStandingUp', 'bigcatgifs', 'catbellies', 'catpictures', 'catpranks', 'catsareliquid', 'catsinsinks', 'catsinbusinessattire', 'catswhoyell', 'catswithjobs', 'cattaps', 'catsisuottafo', 'blep', 'fromkittentocat', 'holdmycatnip', 'jellybeantoes', 'kittens', 'kitting', 'kneadycats', 'mainecoons', 'murdermittens', 'nebelung', 'petthedamncat', 'pocketpussy', 'ragdolls', 'startledcats', 'stuffoncats', 'teefies', 'thecattrapisworking', 'tightpussy', 'toebeans', 'tuckedinkitties']
        self.keyList = ['enter-keys-here']
        self.token = 'enter-token-here'

    # Fetching image
    def image(self, *, breed: Optional[str]):
        if breed:
            response = requests.get(f'https://api.thecatapi.com/v1/images/search?mime_types=jpg,png&breed_ids={breed}', headers={'x-api-key': random.choice(self.keyList)})
            return response.json()
        else:
            response = requests.get('https://api.thecatapi.com/v1/images/search?mime_types=jpg,png', headers={'x-api-key': random.choice(self.keyList)})
            return response.json()

    # Fetching gif
    def gif(self):
        if random.randint(1, 2) == 1:
            response = requests.get('https://api.thecatapi.com/v1/images/search?mime_types=gif', headers={'x-api-key': random.choice(self.keyList)})
            return response.json()
        else:
            response = requests.get('https://edgecats.net/all')
            soup = BeautifulSoup(response.text)
            gifLinks = soup.findAll('a', href=True)
            return random.choice(gifLinks).get('href')

    # Fetching fact
    def fact(self):
        response = requests.get('https://gist.githubusercontent.com/paintingofblue/657d0c4d1202374889ce4a98a6b7f35f/raw/catfacts.txt')
        facts = response.text.splitlines()
        return random.choice(facts)

    # Fetching breeds
    def get_breeds(self):
        response = requests.get('https://api.thecatapi.com/v1/breeds', headers={'x-api-key': random.choice(self.keyList)})
        return response.json()

    # Fetching info about a specific breed
    def get_breed_info(self, breedid: Union[int, str]):
        response = requests.get(f'https://api.thecatapi.com/v1/breeds/{breedid}', headers={'x-api-key': random.choice(self.keyList)})
        return response.json()

# Logger
class Logger:
    """# Logger
    Class used for logging to the console.

    When a function inside of this class is called, it prints using the format of:

    `[+/-/!/*] [time] - [text]`

    ## Methods
    - `append_to_file` `(path: Union[str, Path], text: str)` - Appends text to a file.
    - `write_to_file` `(path: Union[str, Path], text: Union[str, dict], *, json_format='pretty')` - Writes text or a dictionary to a file
    - `info` `(text: str)`
    - `error` `(text: str)`
    - `warning` `(text: str)`
    - `success` `(text: str)`
    """
    def __init__(self):
        self.red: str = '\033[91m'
        self.yellow: str = '\033[93m'
        self.green: str = '\033[92m'
        self.grey: str = '\033[90m'
        self.reset: str = '\033[37m'

    def append_to_file(self, path: Union[str, Path], text: str):
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)

        with open(path, 'a', encoding='utf8') as f:
            f.write(f'{text}\n')

    def write_to_file(self, path: Union[str, Path], text: Union[str, dict], *, json_format='pretty'):
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)

        if type(text) == dict:
            if json_format == 'pretty':
                text = json.dumps(text, indent=4)
            else:
                text = json.dumps(text)

        with open(path, 'w', encoding='utf8') as f:
            f.write(text)

    def info(self, text: str):
        time = datetime.now().strftime("%D %H:%M:%S")
        print(f'{self.grey}[*]{self.reset} {time} - {text}')

    def error(self, text: str):
        time = datetime.now().strftime("%D %H:%M:%S")
        print(f'{self.red}[-]{self.reset} {time} - {text}')

    def warning(self, text: str):
        time = datetime.now().strftime("%D %H:%M:%S")
        print(f'{self.yellow}[!]{self.reset} {time} - {text}')

    def success(self, text: str):
        time = datetime.now().strftime("%D %H:%M:%S")
        print(f'{self.green}[+]{self.reset} {time} - {text}')