from telegram import ReplyKeyboardMarkup

asterisk_keyboard = ReplyKeyboardMarkup(
                    [['menu', 'firewall']],
                    resize_keyboard=True)

back_and_menu = ReplyKeyboardMarkup(
                    [['menu', 'back']],
                    resize_keyboard=True)

command_keyboard = ReplyKeyboardMarkup(
                    [['sh_port', 'sh_mac', 'cab_diag', 'stats'],
                     ['change_ip', 'change_port', 'menu']],
                    resize_keyboard=True)

confirm_kb = ReplyKeyboardMarkup(
                    [['confirm', 'menu', 'back']],
                    resize_keyboard=True)

firewall_keyboard = ReplyKeyboardMarkup(
                    [['menu', 'back'],
                     ['add_ip', 'remove_ip', 'search']],
                    resize_keyboard=True)

menu_keyboard = ReplyKeyboardMarkup(
                    [['switch', 'UPS', 'ping', 'asterisk']],
                    resize_keyboard=True)

ping_keyboard = ReplyKeyboardMarkup(
                    [['ping_again', 'change_ip', 'menu']],
                    resize_keyboard=True)

port_stats_keyboard = ReplyKeyboardMarkup(
                    [['back', 'refresh', 'reset']],
                    resize_keyboard=True)

remove_from_fw_kb = ReplyKeyboardMarkup(
                    [['remove_ip', 'menu', 'back']],
                    resize_keyboard=True)

set_port_keyboard = ReplyKeyboardMarkup(
                    [['change_ip', 'menu']],
                    resize_keyboard=True)

start_keyboard = ReplyKeyboardMarkup(
                    [['start']], resize_keyboard=True)

switch_keyboard = ReplyKeyboardMarkup(
                    [['menu', 'switch_search']],
                    resize_keyboard=True)

to_menu_keyboard = ReplyKeyboardMarkup(
                    [['menu']],
                    resize_keyboard=True)

ups_keyboard = ReplyKeyboardMarkup(
                    [['refresh', 'change_ip', 'menu']],
                    resize_keyboard=True)
