from telegram import ReplyKeyboardMarkup


def start_keyboard():
    return ReplyKeyboardMarkup(
        [['start']], resize_keyboard=True
        )


def menu_keyboard():
    return ReplyKeyboardMarkup(
        [['switch', 'UPS', 'ping', 'asterisk']],
        resize_keyboard=True
        )


def to_menu_keyboard():
    return ReplyKeyboardMarkup(
        [['menu']],
        resize_keyboard=True
        )


back_and_menu = ReplyKeyboardMarkup(
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


ups_keyboard = ReplyKeyboardMarkup(
                [['refresh', 'change_ip', 'menu']],
                resize_keyboard=True
                )

asterisk_keyboard = ReplyKeyboardMarkup(
                        [['menu', 'firewall']],
                        resize_keyboard=True)

firewall_keyboard = ReplyKeyboardMarkup(
                        [['add_ip', 'remove_ip', 'search']],
                        resize_keyboard=True)

remove_from_fw_kb = ReplyKeyboardMarkup(
                        [['remove_ip', 'menu', 'back']],
                        resize_keyboard=True)

add_to_fw_kb = ReplyKeyboardMarkup(
                        [['add_ip', 'menu', 'back']],
                        resize_keyboard=True)
