import time

from telebot import types
from app.settings.bot import bot
from app.utils.api.requests_senders.students import register_student, get_student_username
from app.utils.decorators import bot_command


@bot.message_handler(commands=["start"])
@bot_command
def start_command(message: types.Message):
    def get_username(username_message: types.Message):
        new_username = username_message.text

        register_student(username=new_username, telegram_id=telegram_id)
        nonlocal user_is_registered
        user_is_registered = True

    username = message.from_user.username
    telegram_id = message.from_user.id
    user_is_registered = False

    if not get_student_username(telegram_id):
        if not username:
            sent = bot.send_message(
                telegram_id, "Щоб зареєструватися, потрібно придумати собі нікнейм."
            )
            bot.register_next_step_handler(message=sent, callback=get_username)
            while not user_is_registered:
                time.sleep(0.1)
        else:
            register_student(username=username, telegram_id=telegram_id)

    bot.send_message(
        message.chat.id,
        f"Привіт, {get_student_username(telegram_id)}! Ласкаво просимо до бота для вивчення Пайтону. "
        f"Тисни /help, щоб побачити список команд.",
    )
