from telegram import ReplyKeyboardMarkup


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
