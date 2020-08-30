from service import start_keyboard, get_smile


# start
def whatever(update, context):
    user_name = update._effective_user.first_name
    context.user_data['emoji'] = get_smile(context.user_data)
    update.message.reply_text(f"Hi, {user_name}! {context.user_data['emoji']}\n"
                              "Press start to start",
                              reply_markup=start_keyboard())


# fallback
def wrong_input(update, context):
    update.message.reply_text('Incorrect input')
