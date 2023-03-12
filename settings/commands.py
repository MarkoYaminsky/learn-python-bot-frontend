from telebot.types import BotCommand

general_commands = [
    BotCommand(command="start", description="Розпочати роботу з ботом"),
    BotCommand(command="help", description="Отримати список всіх доступних команд"),
    BotCommand(command="my_group", description="Отримати список студентів зі своєї групи"),
    BotCommand(command="homework", description="Отримати список свого незробленого домашнього завдання"),
    BotCommand(command="submit_homework", description="Подати домашнє завдання на розгляд"),
    BotCommand(command="google_disc", description="Отримати посилання на Гугл диск"),
]

admin_commands = general_commands.copy()
admin_commands.extend([
    BotCommand(command="students_with_undone_homework", description="Побачити всіх студентів з незрозбленим д/з"),
    BotCommand(command="create_group", description="Створити нову групу для студентів"),
    BotCommand(command="add_user_to_group", description="Додати користувачів до групи"),
    BotCommand(command="add_homework", description="Створити домашнє завдання"),
    BotCommand(command="assign_homework", description="Призначити домашнє завдання студентові або групі студентів"),
    BotCommand(command="submitted_homework", description="Перевірити завдання, які подалися на розгляд"),
    BotCommand(command="homework_topics", description="Отримати список тем, з яких було домашнє завдання"),
    BotCommand(command="send_message_from_bot", description="Надіслати повідомлення через бота"),
])
