from connect.asterisk_fw_db import search as fw_search
from connect.asterisk_fw_db import insert as fw_insert
from connect.asterisk_fw_db import delete as fw_delete
from connect.asterisk_fw_db import search_exact
from .keyboard import back_and_menu, asterisk_keyboard
from .keyboard import firewall_keyboard
from .keyboard import confirm_kb
from settings import USER_LIST
from utils import proper_ipif, proper_url


def start(update, context):
    context.user_data['firewall_ip'] = None
    update.message.reply_text('Asterisk menu',
                              reply_markup=asterisk_keyboard)
    return 'asterisk_menu'


def firewall(update, context):
    update.message.reply_text('Что будем делать?',
                              reply_markup=firewall_keyboard)
    return 'asterisk_fw'


def search_ip(update, context):
    update.message.reply_text('Введите IP или подсеть',
                              reply_markup=back_and_menu)
    return 'asterisk_fw_search'


def run_search(update, context):
    ip = update.message.text
    records = fw_search(ip)
    if not records:
        update.message.reply_text(f'Такого IP {ip} нет.',
                                  reply_markup=back_and_menu)
        return 'asterisk_fw_search'
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
    return 'asterisk_fw_search'


def add_start(update, context):
    update.message.reply_text('Введите IP или подсеть',
                              reply_markup=back_and_menu)
    return 'asterisk_fw_add_ip'


def add_ip(update, context):
    ip = update.message.text
    if proper_ipif(ip):
        context.user_data['fw_ip'] = ip
        update.message.reply_text('Теперь название компании',
                                  reply_markup=back_and_menu)
        return 'asterisk_fw_add_client'
    else:
        update.message.reply_text('Это не похоже на правильный IP',
                                  reply_markup=back_and_menu)
        return 'asterisk_fw_add_ip'


def add_client(update, context):
    client = update.message.text
    if len(client) > 100:
        update.message.reply_text('Слишком длинное название',
                                  reply_markup=back_and_menu)
        return 'asterisk_fw_add_client'
    else:
        context.user_data['fw_client'] = client
        update.message.reply_text('И ещё ссылку на заявку',
                                  reply_markup=back_and_menu)
        return 'asterisk_fw_add_url'


def add_url(update, context):
    url = update.message.text
    if (not proper_url(url)) or (len(url) > 100):
        update.message.reply_text('Это не похоже на правильный URL',
                                  reply_markup=back_and_menu)
        return 'asterisk_fw_add_url'
    else:
        context.user_data['fw_url'] = url
        update.message.reply_text('Всё готово. Добавляю?',
                                  reply_markup=confirm_kb)
        return 'asterisk_fw_add_commit'


def add_commit(update, context):
    new_record = fw_insert(
        ip=context.user_data['fw_ip'],
        client=context.user_data['fw_client'],
        url=context.user_data['fw_url'],
        user=USER_LIST[str(update._effective_user.id)]
        )
    if new_record:
        update.message.reply_text('Добавлено.',
                                  reply_markup=firewall_keyboard)
    else:
        update.message.reply_text('Что-то пошло не так.',
                                  reply_markup=firewall_keyboard)
    return 'asterisk_fw'


def del_start(update, context):
    update.message.reply_text('Введите IP или подсеть',
                              reply_markup=back_and_menu)
    return 'asterisk_fw_del_ip'


def del_ip(update, context):
    ip = update.message.text
    existing_record = search_exact(ip)
    if existing_record:
        context.user_data['fw_ip'] = existing_record.ip
        reply = f"{existing_record.ip}\n{existing_record.client}"
        update.message.reply_text(reply + '\nУдаляю?',
                                  reply_markup=confirm_kb)
        return 'asterisk_fw_del_commit'
    else:
        update.message.reply_text('Такого IP нет. Попробуйте ещё раз.',
                                  reply_markup=back_and_menu)
        return 'asterisk_fw_del_start'


def del_commit(update, context):
    ip = context.user_data['fw_ip']
    removed = fw_delete(ip)
    if removed:
        reply = 'Удалено'
    else:
        reply = 'Что-то пошло не так'

    update.message.reply_text(reply, reply_markup=firewall_keyboard)
    return 'asterisk_fw'
