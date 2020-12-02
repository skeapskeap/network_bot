from connect.get_snmp import snmp_reachable, ups_info
from .keyboards import to_menu_keyboard, ups_keyboard
from settings import UPS_COMMUNITY
from utils import proper_host, time_translate


def ups_dialog(update, context):
    context.user_data['ups_ip'] = None
    update.message.reply_text('Set UPS IP-address...',
                              reply_markup=to_menu_keyboard())
    return 'ups_dialog'


def set_ups_ip(update, context):
    ups_ip = update.message.text
    if not proper_host(ups_ip):
        update.message.reply_text('Incorrect IP',
                                  reply_markup=to_menu_keyboard())
        return 'ups_dialog'
    else:
        if snmp_reachable(ups_ip, UPS_COMMUNITY):
            context.user_data['ups_ip'] = ups_ip
            return ups_actions(update, context)
        else:
            update.message.reply_text('SNMP connection error :b',
                                      reply_markup=to_menu_keyboard())
            return 'ups_dialog'


def ups_actions(update, context):
    ups_summmary = ups_info(context.user_data['ups_ip'])
    ups_summmary['runtime'] = time_translate(ups_summmary['runtime'])
    reply_string = ''
    for key, val in ups_summmary.items():
        reply_string += f'{key}: {val}\n'
    update.message.reply_text(reply_string,
                              reply_markup=ups_keyboard)
    return 'ups_actions'
