from emoji import emojize
import random
import re
import settings
import socket
import subprocess
from telegram import ReplyKeyboardMarkup


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
        [['change_ip', 'menu', 'ping_again']],
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
