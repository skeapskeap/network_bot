from service import get_smile, main_keyboard


# /start
def whatever(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    update.message.reply_text(f"Hi! Type /start to start {context.user_data['emoji']}",
                              reply_markup=main_keyboard())


# fallback
def wrong_input(update, context):
    #photo = 'pics/frodo.jpg'
    #chat_id = update.effective_chat.id
    #context.bot.send_photo(chat_id=chat_id, photo=open(photo, 'rb'))
    update.message.reply_text('не знаю такой команды')
