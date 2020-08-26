from emoji import emojize
import random
import re
import settings
from telegram import ReplyKeyboardMarkup


# Выбор смайлика
def get_smile(user_data):
    if 'emoji' not in user_data:
        smile = random.choice(settings.USER_EMOJI)
        return emojize(smile, use_aliases=True)
    return user_data['emoji']


def start_keyboard():
    return ReplyKeyboardMarkup([['/start']], resize_keyboard=True)


def menu_keyboard():
    return ReplyKeyboardMarkup([['switch', 'UPS', 'ping']], resize_keyboard=True)


def to_menu_keyboard():
    return ReplyKeyboardMarkup([['menu']], resize_keyboard=True)


def set_port_keyboard():
    return ReplyKeyboardMarkup([['change_ip', 'menu']], resize_keyboard=True)


def command_keyboard():
    first_row = ['sh_port', 'sh_mac', 'cab_diag']
    second_row = ['change_ip', 'change_port', 'menu']
    return ReplyKeyboardMarkup([first_row, second_row], resize_keyboard=True)


def check_ip(input_data):
    ip = re.search(r'^\d{1,3}[..]\d{1,3}[..]\d{1,3}[..]\d{1,3}$', input_data)
    if not ip:
        return False
    else:
        octets = ip.group(0).split('.')
        for octet in octets:
            if int(octet) > 254:
                return False
        return True


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
