import os
from datetime import datetime
from pathlib import Path
from typing import Union

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