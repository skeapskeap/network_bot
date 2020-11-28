from .keyboards import back_and_menu, to_menu_keyboard, asterisk_keyboard
from .keyboards import add_to_fw_kb, remove_from_fw_kb, menu_keyboard


def asterisk_dialog(update, context):
    update.message.reply_text('Это ещё не работает',
                              reply_markup=menu_keyboard())
    return 'main_menu'

'''
def asterisk_dialog(update, context):
    context.user_data['firewall_ip'] = None
    update.message.reply_text('Asterisk menu',
                              reply_markup=asterisk_keyboard)
    return 'asterisk_menu'
'''

def asterisk_firewall(update, context):
    update.message.reply_text('Введите IP или подсеть',
                              reply_markup=back_and_menu)
    return 'asterisk_firewall'


def search_ip(update, context):
    ip = update.message.text
    ip_exist = False
    if ip_exist:
        context.user_data['firewall_ip'] = ip_exist
        update.message.reply_text(f'Такой IP {ip_exist} уже есть. Удалить?',
                                  reply_markup=remove_from_fw_kb())
    else:
        context.user_data['firewall_ip'] = update.message.text
        update.message.reply_text(f'Такого IP {ip} нет. Добавить?',
                                  reply_markup=add_to_fw_kb())
    return 'asterisk_firewall'


def asterisk_add(update, context):
    ip = context.user_data['firewall_ip']
    proper_ip = False
    if proper_ip:
        update.message.reply_text(f'Добавил {ip} в db',
                                  reply_markup=back_and_menu)
    else:
        update.message.reply_text(f'{ip} это не похоже на IP, попробуйте ещё раз',
                                  reply_markup=back_and_menu)
    return 'asterisk_firewall'


def asterisk_remove(update, context):
    ip = context.user_data['firewall_ip']
    update.message.reply_text(f'Удалил {ip} из db. Удалить ещё что-нибудь?',
                              reply_markup=back_and_menu)
    return 'asterisk_firewall'
