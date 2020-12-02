from emoji import emojize
from logging import handlers
from time import sleep
from validators import url
import logging
import ipaddress
import random
import re
import settings
import socket
import subprocess
import threading


handler = handlers.RotatingFileHandler(
    filename='bot_log', maxBytes=512_000, backupCount=5)
formatter = logging.Formatter(
    '%(asctime)s; %(levelname)s; %(name)s; %(message)s', '%c')
handler.setFormatter(formatter)
logging.basicConfig(level=logging.INFO, handlers=[handler])
logger = logging.getLogger()


# Выбор смайлика
def random_smile():
    smile_name = random.choice(settings.USER_EMOJI)
    emoji = emojize(smile_name, use_aliases=True)
    return emoji


def proper_host(target: str) -> bool:
    try:
        '''если указан домен, проверяет резолвинг его в IP
        если указан ip, проверяет его корректность
        '''
        target = socket.gethostbyname(target)
        return True
    except socket.error:
        return False


def proper_ipif(ip_or_subnet: str) -> bool:
    if not type(ip_or_subnet) is str:
        return False
    try:
        ip = ipaddress.IPv4Interface(ip_or_subnet)
        return ip.is_global
    except (ipaddress.NetmaskValueError,
            ipaddress.AddressValueError):
        return False


def proper_url(input_url: str) -> bool:
    try:
        return url(input_url)
    except TypeError:
        return False


def check_port(input_data):
    port = re.search(r'^\d{1,2}$', input_data)
    if port and (int(port.group(0)) < 53):
        return True
    else:
        return False


def known_user(func):
    def wrapper(update, context):
        user_id = update._effective_user.id
        user_name = update._effective_user.first_name

        if str(user_id) not in settings.USER_LIST.keys():
            update.message.reply_text(
                f'{random_smile()} Хэллоу, {user_name}!\n'
                f'Ваш ID {user_id}\n'
                'Для авторизации скажите его хозяину бота'
                )
            return 'new_user'
        else:
            return func(update, context)

    return wrapper


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
