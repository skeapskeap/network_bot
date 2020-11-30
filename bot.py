from db.renew import renew_db
from dialog import main_menu, whatever, wrong_input
import dialog.asterisk as ast
from dialog.ping import ping_dialog, run_ping, set_ping_ip
from dialog.switch import back_to_commands, clear_stats, port_stats, run_command
from dialog.switch import run_search, set_ip, set_port, switch_search, switch_dialog
from dialog.ups import ups_dialog, set_ups_ip, ups_actions
from telegram.ext import Updater, Filters
from telegram.ext import MessageHandler, ConversationHandler
from utils import EveryHourRun, logger
import settings


def main():
    mybot = Updater(settings.API_KEY, use_context=True)
    dp = mybot.dispatcher

    show_switch = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('^start$'), main_menu)],
        states={
            'main_menu': [
                MessageHandler(Filters.regex('^switch$'), switch_dialog),
                MessageHandler(Filters.regex('^UPS$'), ups_dialog),
                MessageHandler(Filters.regex('^ping$'), ping_dialog),
                MessageHandler(Filters.regex('^asterisk$'), ast.start)],

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

            'asterisk_menu': [
                MessageHandler(Filters.regex('^menu$'), main_menu),
                MessageHandler(Filters.regex('^firewall$'), ast.firewall)],

            'asterisk_firewall': [
                MessageHandler(Filters.regex('^menu$'), main_menu),
                MessageHandler(Filters.regex('^back$'), ast.start),
                MessageHandler(Filters.regex('^search$'), ast.search_ip),
                MessageHandler(Filters.regex('^add_ip$'), ast.add_ip),
                MessageHandler(Filters.regex('^remove_ip$'), ast.remove_ip)],

            'asterisk_firewall_search': [
                MessageHandler(Filters.regex('^menu$'), main_menu),
                MessageHandler(Filters.regex('^back$'), ast.firewall),
                MessageHandler(Filters.text, ast.run_search)],

            },
        fallbacks=[
            MessageHandler(Filters.text | Filters.photo | Filters.video | Filters.document | Filters.location, wrong_input)
        ]
    )
    dp.add_handler(show_switch)
    dp.add_handler(MessageHandler(Filters.text, whatever))
    logger.info('Bot is now running')
    EveryHourRun(renew_db)
    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()
