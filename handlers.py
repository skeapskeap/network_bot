from service import get_smile, start_keyboard


# /start
def whatever(update, context):
    user_name = update._effective_user.first_name
    context.user_data['emoji'] = get_smile(context.user_data)
    update.message.reply_text(f"Hi, {user_name}! {context.user_data['emoji']} \
                                \nType /start to start",
                              reply_markup=start_keyboard())


# fallback
def wrong_input(update, context):
    update.message.reply_text('не знаю такой команды')
