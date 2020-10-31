from service import check_ip, linux_cli
from service import to_menu_keyboard, ping_keyboard


def ping_dialog(update, context):
    context.user_data['ping_ip'] = None
    update.message.reply_text('Set IP to ping...',
                              reply_markup=to_menu_keyboard())
    return 'ping_ip'


def set_ping_ip(update, context):
    ip_to_ping = update.message.text
    if not check_ip(ip_to_ping):  # проверка формата введённых цифр
        update.message.reply_text('Incorrect IP',
                                  reply_markup=to_menu_keyboard())
    else:
        context.user_data['ping_ip'] = ip_to_ping
        run_ping(update, context)
    return 'ping_ip'


def run_ping(update, context):
    ip = context.user_data['ping_ip']
    command = 'ping'

    ping_result = linux_cli(ip, command)
    update.message.reply_text(ping_result, reply_markup=ping_keyboard())
    return 'ping_ip'
