from telegram import ReplyKeyboardRemove
from service import get_smile, menu_keyboard
from service import new_user, start_keyboard


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


# start
def whatever(update, context):
    user_name = update._effective_user.first_name
    context.user_data['emoji'] = get_smile(context.user_data)
    update.message.reply_text(
        f"Hi, {user_name}! {context.user_data['emoji']}\n"
        "Press start to start",
        reply_markup=start_keyboard()
        )


# fallback
def wrong_input(update, context):
    update.message.reply_text('Incorrect input')
