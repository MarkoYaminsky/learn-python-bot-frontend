import datetime

from telebot import types

from settings.bot import bot
from settings.config import ADMINS
from handlers.utils import replace_special_characters, group_tasks_by_username
from utils.api.requests_senders.groups import create_group, add_student_to_group, group_exists
from utils.api.requests_senders.homework import get_homework, add_homework, get_submitted_homework, \
    get_topics
from utils.api.requests_senders.students import get_students_with_undone_homework, get_students_by_group_name, \
    get_student_group, get_student_id
from utils.decorators import bot_command, admin
from settings.commands import general_commands, admin_commands


@bot.message_handler(commands=['help'])
@bot_command
def help_command(message: types.Message):
    commands = general_commands if message.from_user.id not in ADMINS else admin_commands
    response = ''
    for command in commands:
        response += f"/{command.command} - {command.description.lower()}\n"
    bot.send_message(message.chat.id, response.strip())


@bot.message_handler(commands=['my_group'])
@bot_command
def my_group_command(message: types.Message):
    resulting_text = ''
    group_name = get_student_group(student_id := message.chat.id)
    if not group_name:
        bot.send_message(student_id, 'У вас немає групи.')
        return
    students = [student['username'] for student in get_students_by_group_name(group_name)]
    for index, student in enumerate(students, 1):
        resulting_text += f'{index}. @{student}\n'
    bot.send_message(student_id, resulting_text.strip())


@bot.message_handler(commands=['homework'])
@bot_command
def homework_command(message: types.Message):
    resulting_text = ''
    list_of_homework = get_homework(chat_id := message.chat.id)
    for index, homework in enumerate(list_of_homework, 1):
        task = homework['task']
        topic = homework['topic']
        deadline = datetime.datetime.strptime(homework['deadline'], '%Y-%m-%d').strftime('%d.%m.%Y')
        resulting_text += f'Завдання {index} — {topic}.\nЗдати до {deadline} включно.\n\n\n{task}\n\n'
    if list_of_homework:
        last_task = list_of_homework[-1]['task']
        last_row_content = last_task.split('\n')[-1].strip()
        horizontal_indent = '\n' * (2 if last_row_content == '"""' else 3)
        bot.send_message(chat_id, resulting_text.strip()
                         + f"{horizontal_indent}Щоб подати домашнє завдання, використайте /submit_homework")
    else:
        bot.send_message(chat_id, 'Вітаю! У Вас немає домашнього завдання. Ви молодець!')


@bot.message_handler(commands=['submit_homework'])
@bot_command
def submit_homework_command(message: types.Message):
    student_id = message.chat.id
    homework_len = len(homework := get_homework(student_id))
    if homework_len == 0:
        bot.send_message(student_id, "У вас немає незрозбленого домашнього завдання.")
        return
    markup = types.InlineKeyboardMarkup()
    for homework in homework:
        homework_option = types.InlineKeyboardButton(
            homework["topic"],
            callback_data=f'submit_homework {homework["id"]} {student_id}'
        )
        markup.row(homework_option)
    bot.send_message(student_id, "Виберіть тему домашнього завдання.", reply_markup=markup)


@bot.message_handler(commands=['google_disc'])
@bot_command
def google_disc_command(message: types.Message):
    bot.send_message(message.chat.id, 'https://drive.google.com/drive/u/1/folders/1IIKI_kZuBojV07yav6PFNvrS9zEJY-lr')


@bot.message_handler(commands=['students_with_undone_homework'])
@admin
@bot_command
def students_with_undone_homework_command(message: types.Message):
    resulting_text = ''
    this_chat = message.chat.id
    students_and_homework = get_students_with_undone_homework()
    if not students_and_homework:
        bot.send_message(this_chat, 'Всі студенти зробили своє домашнє завдання.')
    grouped_tasks = group_tasks_by_username(students_and_homework)
    for student_index, (username, tasks) in enumerate(grouped_tasks.items(), 1):
        resulting_text += f'Студент {student_index}:\n@{username}\n\nДомашнє завдання:\n'
        for task_index, task in enumerate(tasks, 1):
            resulting_text += f'{student_index}.{task_index}) {task}\n'
        resulting_text += '⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n'
    bot.send_message(this_chat, resulting_text.strip('⎯\n'))


@bot.message_handler(commands=['create_group'])
@admin
@bot_command
def create_group_command(message: types.Message):
    def get_group_name(group_message: types.Message):
        group_name = group_message.text
        group_creation_status = create_group(group_name)
        if group_creation_status != 'success':
            bot.send_message(telegram_id, group_creation_status)
            return
        bot.send_message(telegram_id, f'Успішно створено групу {group_name}.')

    telegram_id = message.chat.id
    sent = bot.send_message(telegram_id, 'Введіть назву нової групи.')
    bot.register_next_step_handler(sent, get_group_name)


@bot.message_handler(commands=['add_user_to_group'])
@admin
@bot_command
def add_user_to_group_command(message: types.Message):
    def get_user_name(user_message: types.Message, group_name):
        user_username = user_message.text
        addition_status = add_student_to_group(student_name=user_username, group_name=group_name)
        if addition_status != 'success':
            bot.send_message(telegram_id, addition_status)
            return
        bot.send_message(get_student_id(user_username), f'Вас додано до групи {group_name}.')
        bot.send_message(telegram_id, f'Успішно додано користувача @{user_username} до групи {group_name}')

    def get_group_name(group_message: types.Message):
        group_name = group_message.text
        if not group_exists(group_name):
            bot.send_message(telegram_id, f'Групи з назвою {group_name} не існує.')
            return
        sent_user = bot.send_message(telegram_id, 'Введіть псевдонім користувача, якого хочете додати.')
        bot.register_next_step_handler(sent_user, get_user_name, group_name=group_name)

    telegram_id = message.chat.id
    sent_group = bot.send_message(telegram_id, 'Введіть назву групи, в яку хочете додати.')
    bot.register_next_step_handler(sent_group, get_group_name)


@bot.message_handler(commands=['add_homework'])
@admin
@bot_command
def add_homework_command(message: types.Message):
    def get_topic(topic_message: types.Message):
        topic = topic_message.text
        sent_task = bot.send_message(chat_id, 'Введіть вміст домашнього завдання.')
        bot.register_next_step_handler(sent_task, get_task, topic)

    def get_task(task_message: types.Message, topic: str):
        task = replace_special_characters(task_message.text)
        addition_details = add_homework(topic=topic, task=task)
        if addition_details != 'success':
            bot.send_message(chat_id, addition_details)
            return
        bot.send_message(chat_id, f'Успішно додано нове домашнє завдання з темою "{topic}".')

    chat_id = message.chat.id
    sent_topic = bot.send_message(chat_id, 'Введіть тему домашнього завдання.')
    bot.register_next_step_handler(sent_topic, get_topic)


@bot.message_handler(commands=['assign_homework'])
@admin
@bot_command
def assign_homework_command(message: types.Message):
    markup = types.InlineKeyboardMarkup()
    group_option = types.InlineKeyboardButton('Групі', callback_data='assign_to_group')
    personal_option = types.InlineKeyboardButton('Студенту', callback_data='assign_to_student')
    markup.row(group_option, personal_option)
    bot.send_message(message.chat.id, "Кому Ви хочете призначити домашнє завдання?", reply_markup=markup)


@bot.message_handler(commands=['submitted_homework'])
@admin
@bot_command
def submitted_homework_command(message: types.Message):
    homework_data = get_submitted_homework()
    if not homework_data:
        bot.send_message(message.chat.id, 'На зараз ніхто не подав домашнє завдання на розгляд.')
        return
    for item in homework_data:
        content = item['content']
        student = item['student']
        homework = item['homework']

        student_id = student['telegramId']
        student_name = student['username']
        homework_id = homework['id']
        task = homework['task']

        approve_option = types.InlineKeyboardButton('Прийняти', callback_data=f'approve {student_id} {homework_id}')
        decline_option = types.InlineKeyboardButton('Відхилити', callback_data=f'decline {student_id} {homework_id}')
        markup = types.InlineKeyboardMarkup()
        markup.row(approve_option, decline_option)

        bot.send_message(
            message.chat.id,
            f'Студент: @{student_name}\n\n'
            f'Завдання:\n{task}\n\n'
            f'Розв\'язок:\n{content}',
            reply_markup=markup
        )


@bot.message_handler(commands=['homework_topics'])
@admin
@bot_command
def homework_topics_command(message: types.Message):
    topics = get_topics()
    resuting_message = ''
    for index, topic in enumerate(topics, 1):
        resuting_message += f'{index}. {topic}\n'
    bot.send_message(message.chat.id, resuting_message.strip())


@bot.message_handler(commands=['remind_students'])
@admin
@bot_command
def remind_students_command(message: types.Message):
    students_to_remind = group_tasks_by_username(get_students_with_undone_homework())
    for student_name, homework in students_to_remind.items():
        reminder_message = 'Нагадування!\nУ вас не зроблені такі домашні завдання:\n\n'
        for task_index, task in enumerate(homework, 1):
            reminder_message += f'{task_index}) {task}\n'
        reminder_message += '\nЩоб побачити деталі, введіть /homework.'
        bot.send_message(get_student_id(student_name), reminder_message)
