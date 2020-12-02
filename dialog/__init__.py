from .keyboard import start_keyboard, menu_keyboard
from utils import known_user, random_smile


@known_user
def main_menu(update, context):
    context.user_data['have_ip'] = False
    context.user_data['have_port'] = False
    context.user_data['have_stats'] = False
    update.message.reply_text(
        f"{random_smile()} Вы находитесь в главном меню",
        reply_markup=menu_keyboard
        )
    return 'main_menu'


# start
@known_user
def whatever(update, context):
    user_name = update._effective_user.first_name
    update.message.reply_text(
        f"{random_smile()} Привет, {user_name}!\n"
        "Нажми на start",
        reply_markup=start_keyboard
        )


# fallback
def wrong_input(update, context):
    update.message.reply_text(f'{random_smile()} Некорректный запрос')
