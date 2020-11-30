from connect.asterisk_fw_db import search as fw_search
from .keyboards import back_and_menu, to_menu_keyboard, asterisk_keyboard
from .keyboards import firewall_keyboard
from .keyboards import add_to_fw_kb, remove_from_fw_kb, menu_keyboard

'''
def asterisk_dialog(update, context):
    update.message.reply_text('Это ещё не работает',
                              reply_markup=menu_keyboard())
    return 'main_menu'

'''
def start(update, context):
    context.user_data['firewall_ip'] = None
    update.message.reply_text('Asterisk menu',
                              reply_markup=asterisk_keyboard)
    return 'asterisk_menu'


def firewall(update, context):
    update.message.reply_text('Что будем делать?',
                              reply_markup=firewall_keyboard)
    return 'asterisk_firewall'


def search_ip(update, context):
    update.message.reply_text('Введите IP или подсеть',
                              reply_markup=back_and_menu)
    return 'asterisk_firewall_search'


def run_search(update, context):
    ip = update.message.text
    records = fw_search(ip)
    if not records:
        return not_found(update, context, ip)
    return records_found(update, context, records)


def records_found(update, context, records):
    if len(records) > 10:
        reply_text = ('Слишком много нашлось\n'
                      'Уточните запрос.')
    else:
        reply_text = 'Вот, что я нашла:\n'
        for record in records:
            reply_text += f"{record['ip']} - {record['client']}\n"
    update.message.reply_text(reply_text,
                              reply_markup=back_and_menu)
    return 'asterisk_firewall_search'


def not_found(update, context, ip):
    proper_ip = True
    #if proper_ip(ip):
    if proper_ip:
        context.user_data['firewall_ip'] = ip
        update.message.reply_text(f'Такого IP {ip} нет. Добавить?',
                                  reply_markup=add_to_fw_kb)
    else:
        update.message.reply_text(f'Такого IP {ip} нет.',
                                  reply_markup=back_and_menu)
    return 'asterisk_firewall'


def add_ip(update, context):
    proper_ip = True
    ip = context.user_data['firewall_ip']
    if proper_ip:
        update.message.reply_text(f'Добавил {ip} в db',
                                  reply_markup=back_and_menu)
    return 'asterisk_firewall'


def remove_ip(update, context):
    ip = context.user_data['firewall_ip']
    update.message.reply_text(f'Удалил {ip} из db. Удалить ещё что-нибудь?',
                              reply_markup=back_and_menu)
    return 'asterisk_firewall'
