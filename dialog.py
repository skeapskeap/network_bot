from telegram import ReplyKeyboardRemove
from service import menu_keyboard
from service import new_user


def main_menu(update, context):
    user_id = update._effective_user.id
    user_name = update._effective_user.first_name
    if new_user(user_id):
        update.message.reply_text(
            f'Hi, {user_name}! Your ID is {user_id}',
            reply_markup=ReplyKeyboardRemove()
            )
        return 'new_user'
    else:
        context.user_data['have_ip'] = False
        context.user_data['have_port'] = False
        context.user_data['have_stats'] = False
        update.message.reply_text(
            "You're now in main menu",
            reply_markup=menu_keyboard()
            )
        return 'main_menu'
