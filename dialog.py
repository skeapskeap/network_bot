from get_snmp import choose_cmd
from telegram import ReplyKeyboardRemove
from service import main_keyboard, command_keyboard, set_port_keyboard
from service import check_ip, check_port


def switch_dialog(update, context):
    context.user_data['have_ip'] = False
    context.user_data['have_port'] = False
    update.message.reply_text('введите IP', reply_markup=ReplyKeyboardRemove())
    return 'set_ip'


def set_ip(update, context):
    user_reply = update.message.text
    if context.user_data['have_port']:
        return ask_port(update, context)

    if check_ip(user_reply):
        context.user_data['selected_ip'] = user_reply
        context.user_data['have_ip'] = True
        return ask_port(update, context)
    else:
        update.message.reply_text('некорректный IP')
        return 'set_ip'


def ask_port(update, context):
    update.message.reply_text(f'selected_ip = {context.user_data["selected_ip"]}')
    update.message.reply_text('введите порт', reply_markup=set_port_keyboard())
    return 'set_port'


def set_port(update, context):
    user_reply = update.message.text
    if check_port(user_reply):
        context.user_data['selected_port'] = user_reply
        context.user_data['have_port'] = True
        update.message.reply_text(f'ip = {context.user_data["selected_ip"]}, '
                                  f'port = {context.user_data["selected_port"]}',
                                  reply_markup=command_keyboard())
        return 'commands'
    else:
        update.message.reply_text('некорректный порт', reply_markup=set_port_keyboard())
        return 'set_port'


def run_command(update, context):
    command = update.message.text
    ip = context.user_data["selected_ip"]
    port = context.user_data["selected_port"]

    switch_reply = choose_cmd(ip, port, command)
    update.message.reply_text(switch_reply)
    return 'commands'


def clear(update, context):
    context.user_data.clear()
    update.message.reply_text('Loged out', reply_markup=main_keyboard())
