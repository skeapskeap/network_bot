from emoji import emojize
from telegram import ReplyKeyboardMarkup
from time import sleep
import logging
from logging import handlers
import random
import re
import settings
import socket
import subprocess
import threading


handler = handlers.RotatingFileHandler(
    filename='log', maxBytes=512_000, backupCount=5)
formatter = logging.Formatter(
    '%(asctime)s; %(levelname)s; %(name)s; %(message)s', '%c')
handler.setFormatter(formatter)
logging.basicConfig(level=logging.INFO, handlers=[handler])
logger = logging.getLogger()


# Выбор смайлика
def get_smile(user_data):
    if 'emoji' not in user_data:
        smile = random.choice(settings.USER_EMOJI)
        return emojize(smile, use_aliases=True)
    return user_data['emoji']


def start_keyboard():
    return ReplyKeyboardMarkup(
        [['start']], resize_keyboard=True
        )


def menu_keyboard():
    return ReplyKeyboardMarkup(
        [['switch', 'UPS', 'ping']],
        resize_keyboard=True
        )


def to_menu_keyboard():
    return ReplyKeyboardMarkup(
        [['menu']],
        resize_keyboard=True
        )


def back_and_menu():
    return ReplyKeyboardMarkup(
        [['menu', 'back']],
        resize_keyboard=True
        )


def switch_keyboard():
    return ReplyKeyboardMarkup(
        [['menu', 'switch_search']],
        resize_keyboard=True
        )


def set_port_keyboard():
    return ReplyKeyboardMarkup(
        [['change_ip', 'menu']],
        resize_keyboard=True
        )


def port_stats_keyboard():
    return ReplyKeyboardMarkup(
        [['back', 'refresh', 'reset']],
        resize_keyboard=True
        )


def command_keyboard():
    first_row = ['sh_port', 'sh_mac', 'cab_diag', 'stats']
    second_row = ['change_ip', 'change_port', 'menu']

    return ReplyKeyboardMarkup(
        [first_row, second_row],
        resize_keyboard=True
        )


def ping_keyboard():
    return ReplyKeyboardMarkup(
        [['ping_again', 'change_ip', 'menu']],
        resize_keyboard=True
        )


def ups_keyboard():
    return ReplyKeyboardMarkup(
        [['refresh', 'change_ip', 'menu']],
        resize_keyboard=True
        )


def check_ip(target: str) -> bool:
    try:
        '''если указан домен, проверяет резолвинг его в IP
        если указан ip, проверяет его корректность
        '''
        target = socket.gethostbyname(target)
        return True
    except socket.error:
        return False


def check_port(input_data):
    port = re.search(r'^\d{1,2}$', input_data)
    if port and (int(port.group(0)) < 53):
        return True
    else:
        return False


def new_user(user_id):
    if str(user_id) not in settings.USER_LIST:
        return True
    else:
        return False


def linux_cli(target: str, command: str) -> str:
    query = [command, target, '-c 4']
    try:
        result = subprocess.check_output(
            query, universal_newlines=True, stderr=subprocess.STDOUT
            )
    except FileNotFoundError as no_file:
        result = f'{no_file.filename}: {no_file.strerror}'
    except subprocess.CalledProcessError as proc_err:
        result = proc_err.output
    return result


def time_translate(time: int) -> str:
    seconds = time // 100
    minutes, hours, days = 0, 0, 0
    if seconds > 60:
        minutes = seconds // 60
        time = f'{minutes}min'
    if minutes > 60:
        hours = minutes // 60
        minutes = minutes % 60
        time = f'{hours}hr {minutes}min'
    if hours > 24:
        days = hours // 24
        hours = hours % 24
        time = f'{days}d {hours}hr {minutes}min'
    return time


class EveryHourRun():

    def __init__(self, func):
        self.func = func
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        while True:
            self.func()
            sleep(3600)
