import os
import requests
import random
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
import os
from datetime import datetime
from pathlib import Path

class Logger:
    def __init__(self):
        self.red = '\033[91m'
        self.yellow = '\033[93m'
        self.green = '\033[92m'
        self.grey = '\033[90m'
        self.reset = '\033[37m'

    def append_to_file(self, file_path: str | Path | os.PathLike, text: str | dict, encoding: str='utf8'):
        path = Path(file_path).parent
        path.mkdir(parents=True, exist_ok=True)

        try:
            with open(file_path, 'a', encoding=encoding) as f:
                f.write(f'{text}\n')
        except PermissionError as e:
            raise PermissionError(f'Unable to write to {file_path}, as permission was denied.')
        except OSError as e:
            raise OSError(f'Unable to write to {file_path}, as the OS returned an error: {e.strerror}')

    def fetch_time(self, time: Union[datetime, int, float] = datetime.now(), time_format='now') -> str:
        allowed_formats = ['now', 'date', 'date-alt', 'full']
        if time_format not in allowed_formats:
            time_format = allowed_formats[0]

        if type(time) == Union[int, float]:
            time = datetime.fromtimestamp(time)

        match time_format:
            case 'now':
                time = datetime.now().strftime('%H:%M:%S')
            case 'date':
                time = time.strftime('%d/%m/%Y')
            case 'date-alt':
                time = time.strftime('%d-%m-%Y')
            case 'full':
                time = time.strftime('%d/%m/%Y %H:%M:%S')

        return time

    def info(self, text: str, write: bool = False):
        time = datetime.now()

        console_time = self.fetch_time()
        console_text = f'[{console_time}] {self.grey}[~]{self.reset} {text}'
        print(console_text)

        if write:
            current_date = self.fetch_time(time=time, time_format='date-alt')
            file_time = self.fetch_time(time=time)
            file_text = f'[{file_time}] [INFO] {text}'
            self.append_to_file(f'logs/{current_date}.log', file_text)

    def success(self, text: str, write: bool = False):
        time = datetime.now()

        console_time = self.fetch_time()
        console_text = f'[{console_time}] {self.green}[+]{self.reset} {text}'
        print(console_text)

        if write:
            current_date = self.fetch_time(time=time, time_format='date-alt')
            file_time = self.fetch_time(time=time)
            file_text = f'[{file_time}] [SUCCESS] {text}'
            self.append_to_file(f'logs/{current_date}.log', file_text)

    def error(self, text: str, write: bool = False):
        time = datetime.now()

        console_time = self.fetch_time()
        console_text = f'[{console_time}] {self.red}[-]{self.reset} {text}'
        print(console_text)

        if write:
            current_date = self.fetch_time(time=time, time_format='date-alt')
            file_time = self.fetch_time(time=time)
            file_text = f'[{file_time}] [ERROR] {text}'
            self.append_to_file(f'logs/{current_date}.log', file_text)

    def warning(self, text: str, write: bool = False):
        time = datetime.now()

        console_time = self.fetch_time()
        console_text = f'[{console_time}] {self.yellow}[!]{self.reset} {text}'
        print(console_text)

        if write:
            current_date = self.fetch_time(time=time, time_format='date-alt')
            file_time = self.fetch_time(time=time)
            file_text = f'[{file_time}] [WARNING] {text}'
            self.append_to_file(f'logs/{current_date}.log', file_text)