from get_snmp import choose_cmd
from telegram import ReplyKeyboardRemove
from service import start_keyboard, menu_keyboard, command_keyboard, set_port_keyboard, to_menu_keyboard
from service import check_ip, check_port, new_user


def main_menu(update, context):
    user_id = update._effective_user.id
    user_name = update._effective_user.first_name
    if new_user(user_id):
        update.message.reply_text(f'Hi, {user_name}! Your ID is {user_id}', reply_markup=ReplyKeyboardRemove())
        return 'new_user'
    else:
        update.message.reply_text("You're now in main menu", reply_markup=menu_keyboard())
        return 'main_menu'


def switch_dialog(update, context):
    context.user_data['have_ip'] = False
    context.user_data['have_port'] = False
    update.message.reply_text('введите IP', reply_markup=to_menu_keyboard())
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
        update.message.reply_text('некорректный IP', reply_markup=to_menu_keyboard())
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


def ups_dialog(update, context):
    update.message.reply_text('это ещё не работает', reply_markup=menu_keyboard())
    return 'main_menu'


def ping_dialog(update, context):
    update.message.reply_text('это ещё не работает', reply_markup=menu_keyboard())
    return 'main_menu'


def clear(update, context):
    context.user_data.clear()
    update.message.reply_text('Loged out', reply_markup=start_keyboard())
