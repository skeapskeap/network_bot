from dialog import main_menu
from dialog_ping import ping_dialog, run_ping, set_ping_ip
from dialog_switch import back_to_commands, clear_stats, port_stats, run_command
from dialog_switch import run_search, set_ip, set_port, switch_search, switch_dialog
from dialog_ups import ups_dialog, set_ups_ip, ups_actions
from handlers import whatever, wrong_input
import logging
import settings
from telegram.ext import Updater, Filters
from telegram.ext import MessageHandler, ConversationHandler


logging.basicConfig(filename='bot_log', level=logging.INFO)


def main():
    mybot = Updater(settings.API_KEY, use_context=True)
    dp = mybot.dispatcher

    show_switch = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('^start$'), main_menu)],
        states={
            'main_menu': [
                MessageHandler(Filters.regex('^switch$'), switch_dialog),
                MessageHandler(Filters.regex('^UPS$'), ups_dialog),
                MessageHandler(Filters.regex('^ping$'), ping_dialog)],

            'set_ip': [
                MessageHandler(Filters.regex('^menu$'), main_menu),
                MessageHandler(Filters.regex('^switch_search$'), switch_search),
                MessageHandler(Filters.text, set_ip)],

            'search_menu': [
                MessageHandler(Filters.regex('^menu$'), main_menu),
                MessageHandler(Filters.regex('^back$'), switch_dialog),
                MessageHandler(Filters.text, run_search)],

            'set_port': [
                MessageHandler(Filters.regex('^menu$'), main_menu),
                MessageHandler(Filters.regex('^change_ip$'), switch_dialog),
                MessageHandler(Filters.text, set_port)],

            'commands': [
                MessageHandler(Filters.regex('^menu$'), main_menu),
                MessageHandler(Filters.regex('^change_ip$'), switch_dialog),
                MessageHandler(Filters.regex('^change_port$'), set_ip),
                MessageHandler(Filters.regex('^sh_port$'), run_command),
                MessageHandler(Filters.regex('^sh_mac$'), run_command),
                MessageHandler(Filters.regex('^cab_diag$'), run_command),
                MessageHandler(Filters.regex('^stats$'), port_stats)],

            'port_stats': [
                MessageHandler(Filters.regex('^back$'), back_to_commands),
                MessageHandler(Filters.regex('^refresh$'), port_stats),
                MessageHandler(Filters.regex('^reset$'), clear_stats)],

            'ping_ip': [
                MessageHandler(Filters.regex('^menu$'), main_menu),
                MessageHandler(Filters.regex('^change_ip$'), ping_dialog),
                MessageHandler(Filters.regex('^ping_again$'), run_ping),
                MessageHandler(Filters.text, set_ping_ip)],

            'ups_dialog': [
                MessageHandler(Filters.regex('^menu$'), main_menu),
                MessageHandler(Filters.text, set_ups_ip)],

            'ups_actions': [
                MessageHandler(Filters.regex('^menu$'), main_menu),
                MessageHandler(Filters.regex('^change_ip$'), ups_dialog),
                MessageHandler(Filters.regex('^refresh$'), ups_actions)],
            },
        fallbacks=[
            MessageHandler(Filters.text | Filters.photo | Filters.video | Filters.document | Filters.location, wrong_input)
        ]
    )
    dp.add_handler(show_switch)
    dp.add_handler(MessageHandler(Filters.text, whatever))
    logging.info('Bot is now running')
    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()
