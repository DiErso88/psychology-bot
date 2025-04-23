from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes
import os

# Этапы разговора
NAME, REQUEST, TIME = range(3)

# Telegram ID, куда отправлять заявки
ADMIN_ID = 985810567  # Замените на свой Telegram ID

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [["📅 Записаться на консультацию"], ["ℹ️ Обо мне", "❓ Частые вопросы"], ["📚 Полезные материалы", "✉️ Связаться напрямую"]]
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    await update.message.reply_text(
        "Здравствуйте! Я — Закия, практикующий психолог. Здесь вы можете узнать обо мне и записаться на сессию.",
        reply_markup=reply_markup
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "📅 Записаться на консультацию":
        await update.message.reply_text("Как вас зовут?")
        return NAME
    elif text == "ℹ️ Обо мне":
        await update.message.reply_text("Здравствуйте, меня зовут Закия. Я - практикующий психолог с двумя высшими образованиями, в том числе юридическим. Поэтому оказываю всестороннюю поддержку, включая правовые вопросы гражданского характера. Член Европейской Ассоциации Транзактного анализа, Санкт-Петербургской Организации Транзактного Анализа. Постоянно обучаюсь, прохожу личную терапию и супервизии.")
    elif text == "❓ Частые вопросы":
        await update.message.reply_text("1. Сессия длится 50 минут.\n2. Проходит очно в Краснодаре, онлайн в Zoom или Telegram.\n3. Первая встреча — для знакомства и запроса. \n4. Стоимость сессии - 4000 рублей.")
    elif text == "📚 Полезные материалы":
        await update.message.reply_text("Здесь вы можете ознакомиться с моими статьями по психологии: https://www.b17.ru/id986545/")
    elif text == "✉️ Связаться напрямую":
        await update.message.reply_text("Мой Telegram: @SenZakiya")
    else:
        await update.message.reply_text("Пожалуйста, выберите пункт из меню.")

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['name'] = update.message.text
    await update.message.reply_text("Кратко расскажите, с чем вы хотите обратиться (тревога, стресс, отношения, другое)?")
    return REQUEST

async def get_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['request'] = update.message.text
    await update.message.reply_text("Когда вам удобно со мной связаться? (будни/выходные, утро/день/вечер)")
    return TIME

async def get_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['time'] = update.message.text

    message = (
        "✨ Новая заявка на консультацию:\n\n"
        f"Имя: {context.user_data['name']}\n"
        f"Запрос: {context.user_data['request']}\n"
        f"Удобное время: {context.user_data['time']}\n\n"
        f"👉 Написать: @{update.effective_user.username if update.effective_user.username else 'пользователь скрыл username'}"
    )
    await context.bot.send_message(chat_id=ADMIN_ID, text=message)
    await update.message.reply_text("Спасибо! Я получила ваш запрос и скоро свяжусь с вами 🕊️")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Отменено. Если захотите начать сначала — нажмите 'Записаться на консультацию'.")
    return ConversationHandler.END

if __name__ == '__main__':
    app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^📅 Записаться на консультацию$"), handle_message)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            REQUEST: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_request)],
            TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_time)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Бот запущен")
    app.run_polling()
