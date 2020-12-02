from db.renew import renew_db
from telegram.ext import Updater, Filters
from telegram.ext import MessageHandler, ConversationHandler
from utils import EveryHourRun, logger
import dialog as dg
import dialog.states as states
import settings


def main():
    mybot = Updater(settings.API_KEY, use_context=True)
    dp = mybot.dispatcher

    show_switch = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('^start$'), dg.main_menu)
            ],
        states={
            'main_menu': states.main_menu,
            'switch_ip': states.switch_ip,
            'switch_search': states.switch_search,
            'switch_port': states.switch_port,
            'switch_commands': states.switch_commands,
            'switch_port_stats': states.switch_port_stats,
            'ping_ip': states.ping_ip,
            'ups_ip': states.ups_ip,
            'ups_actions': states.ups_actions,
            'asterisk_menu': states.asterisk_menu,
            'asterisk_fw': states.asterisk_fw,
            'asterisk_fw_search': states.asterisk_fw_search,
            'asterisk_fw_add_ip': states.asterisk_fw_add_ip,
            'asterisk_fw_add_client': states.asterisk_fw_add_client,
            'asterisk_fw_add_url': states.asterisk_fw_add_url,
            'asterisk_fw_add_commit': states.asterisk_fw_add_commit,
            'asterisk_fw_del_ip': states.asterisk_fw_del_ip,
            'asterisk_fw_del_commit': states.asterisk_fw_del_commit
            },
        fallbacks=[
            MessageHandler(Filters.text | Filters.photo | Filters.video | Filters.document | Filters.location, dg.wrong_input)
            ]
    )

    dp.add_handler(show_switch)
    dp.add_handler(MessageHandler(Filters.text, dg.whatever))
    logger.info('Bot is now running')
    EveryHourRun(renew_db)
    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()
