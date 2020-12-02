from connect.get_snmp import choose_cmd, get_port_stats
from connect.get_snmp import sh_port, snmp_reachable
from db.search import search_in_db
from .keyboard import back_and_menu, command_keyboard, port_stats_keyboard
from .keyboard import switch_keyboard, set_port_keyboard, to_menu_keyboard
from settings import SW_COMMUNITY
from time import time
from utils import proper_host, check_port


def dialog(update, context):
    context.user_data['have_ip'] = False
    context.user_data['have_port'] = False
    update.message.reply_text(
        'Set IP...',
        reply_markup=switch_keyboard)
    return 'switch_ip'


def search(update, context):
    update.message.reply_text(
        'Введите адрес или название, или часть названия.'
        'Ну хоть что-нибудь. Через пробел пожалуйста.',
        reply_markup=back_and_menu
        )
    return 'switch_search'


def run_search(update, context):
    words = update.message.text
    result = search_in_db(words)
    update.message.reply_text(
        result,
        reply_markup=back_and_menu
    )
    return 'switch_search'


def set_ip(update, context):
    ip = update.message.text
    if context.user_data['have_port']:
        return ask_port(update, context)

    if not proper_host(ip):  # проверка формата введённых цифр
        update.message.reply_text(
            'Incorrect IP',
            reply_markup=to_menu_keyboard)
        return 'switch_ip'

    # проверка того, что ip доступен по SNMP
    if snmp_reachable(ip, SW_COMMUNITY):
        context.user_data['switch_model'] = snmp_reachable(ip, SW_COMMUNITY)
        context.user_data['selected_ip'] = ip
        context.user_data['have_ip'] = True
        return ask_port(update, context)
    else:
        update.message.reply_text(
            'Host unreachable with SNMP',
            reply_markup=to_menu_keyboard)
        return 'switch_ip'


def ask_port(update, context):
    update.message.reply_text(
        f'{context.user_data["switch_model"]}\n'
        f'ip: {context.user_data["selected_ip"]}\n'
        'Set port...', reply_markup=set_port_keyboard)
    return 'switch_port'


def set_port(update, context):
    ip = context.user_data["selected_ip"]
    port = update.message.text
    if check_port(port) and sh_port(ip, port):
        context.user_data['selected_port'] = port
        context.user_data['have_port'] = True
        update.message.reply_text(
            f'ip: {context.user_data["selected_ip"]}\n'
            f'port: {context.user_data["selected_port"]}',
            reply_markup=command_keyboard)
        return 'switch_commands'
    else:
        update.message.reply_text(
            f'Incorrect port for {context.user_data["switch_model"]}',
            reply_markup=set_port_keyboard)
        return 'switch_port'


def run_command(update, context):
    command = update.message.text
    ip = context.user_data["selected_ip"]
    port = context.user_data["selected_port"]

    switch_reply = choose_cmd(ip, port, command)
    update.message.reply_text(switch_reply)
    return 'switch_commands'


def port_stats(update, context):
    ip = context.user_data["selected_ip"]
    port = context.user_data["selected_port"]

    if not get_port_stats(ip, port):  # если хост перестал отвечать на SNMP
        update.message.reply_text('SNMP error',
                                  reply_markup=port_stats_keyboard)
        return 'switch_port_stats'
    else:
        rx_bytes, tx_bytes, crc_err = get_port_stats(ip, port)

    if context.user_data['have_stats']:
        time_delta = int(time()) - context.user_data['start_time']
        rx_rate = (rx_bytes - context.user_data['rx_bytes']) // time_delta
        tx_rate = (tx_bytes - context.user_data['tx_bytes']) // time_delta
        rx_rate_mbps = rx_rate * 8 / 1024 / 1024
        tx_rate_mbps = tx_rate * 8 / 1024 / 1024
        update.message.reply_text(
            f'Average in {time_delta} seconds:\n'
            f'  rx_rate: {round(rx_rate_mbps, 2)} mbit/s,\n'
            f'  tx_rate: {round(tx_rate_mbps, 2)} mbit/s,\n'
            f'Total crc: {crc_err}',
            reply_markup=port_stats_keyboard)
    else:
        context.user_data['start_time'] = int(time())  # unix time in seconds
        context.user_data['rx_bytes'] = rx_bytes
        context.user_data['tx_bytes'] = tx_bytes
        context.user_data['have_stats'] = True
        update.message.reply_text(
            'Ok, GO. Press "refresh"',
            reply_markup=port_stats_keyboard)
    return 'switch_port_stats'


def back_to_commands(update, context):
    context.user_data['have_stats'] = False
    update.message.reply_text(
        f'ip: {context.user_data["selected_ip"]}\n'
        f'port: {context.user_data["selected_port"]}',
        reply_markup=command_keyboard)
    return 'switch_commands'


def clear_stats(update, context):
    context.user_data['have_stats'] = False
    update.message.reply_text(
        'Delete stats. Press "refresh"',
        reply_markup=port_stats_keyboard)
