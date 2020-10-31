from service import menu_keyboard


def ups_dialog(update, context):
    update.message.reply_text(
        'это ещё не работает',
        reply_markup=menu_keyboard()
        )
    return 'main_menu'
