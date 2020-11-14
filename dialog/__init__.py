from service import random_smile, menu_keyboard
from service import known_user, start_keyboard


@known_user
def main_menu(update, context):
    context.user_data['have_ip'] = False
    context.user_data['have_port'] = False
    context.user_data['have_stats'] = False
    update.message.reply_text(
        f"{random_smile()} Вы находитесь в главном меню",
        reply_markup=menu_keyboard()
        )
    return 'main_menu'


# start
@known_user
def whatever(update, context):
    user_name = update._effective_user.first_name
    update.message.reply_text(
        f"{random_smile()} Привет, {user_name}!\n"
        "Press start to start",
        reply_markup=start_keyboard()
        )


# fallback
def wrong_input(update, context):
    update.message.reply_text(f'{random_smile()} Incorrect input')
