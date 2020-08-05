from service import get_smile, main_keyboard


# /start
def whatever(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    update.message.reply_text(f"Hi! Type /start to start {context.user_data['emoji']}",
                              reply_markup=main_keyboard())
