import datetime

from telebot import types

from settings import commands
from settings.bot import bot
from settings.config import ADMINS


def logged(function):
    def wrapper(*args, **kwargs):
        with open("logs", "a") as file:
            username = kwargs.get("username", None)
            time_now = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            file.write(
                function.__name__
                + (f" - {username}" if username else "")
                + f" | {time_now}\n"
            )
            return function(*args, **kwargs)

    return wrapper


def admin(function):
    def wrapper(message: types.Message):
        if message.chat.id not in ADMINS:
            return
        function(message)

    return wrapper


def bot_command(function):
    from utils.api.requests_senders.students import update_student
    from utils.api.requests_senders.students import get_student_username

    def wrapper(message: types.Message):
        bot.set_my_commands(commands.general_commands)
        username = message.from_user.username
        telegram_id = message.from_user.id
        student_name_in_db = get_student_username(message.chat.id)
        if username != student_name_in_db and student_name_in_db:
            update_student(telegram_id=telegram_id, username=username)
        function(message)

    return wrapper
