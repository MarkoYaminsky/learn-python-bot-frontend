from telebot import types

from settings.bot import bot
from handlers.utils import assignment_with_option, replace_special_characters
from settings.config import MY_USER_ID
from utils.api.requests_senders.homework import approve_or_decline_homework, get_topic, submit_homework
from utils.api.requests_senders.students import get_student_username


@bot.callback_query_handler(lambda query: query.data in ['assign_to_group', 'assign_to_student'])
def assign_to_group_or_student_callback(query: types.CallbackQuery):
    if query.data == 'assign_to_group':
        assignment_with_option('group', query.from_user.id)
    else:
        assignment_with_option('student', query.from_user.id)


@bot.callback_query_handler(lambda query: query.data.startswith('approve') or query.data.startswith('decline'))
def approve_or_decline_homework_callback(query: types.CallbackQuery):
    _, student_id, homework_id = query.data.split()
    student_id, homework_id = map(int, (student_id, homework_id))
    topic = get_topic(homework_id)
    if query.data.split()[0] == 'approve':
        approve_or_decline_homework(option='approve', student_id=student_id, homework_id=homework_id)
        bot.send_message(query.from_user.id, 'Прийнято.')
        bot.send_message(student_id, f'Ваше домашнє завдання з теми "{topic}" прийнято.')
    else:
        approve_or_decline_homework(option='decline', student_id=student_id, homework_id=homework_id)
        bot.send_message(query.from_user.id, 'Відхилено.')
        bot.send_message(student_id, f'Ваше домашнє завдання з теми "{topic}" відхилено.')


@bot.callback_query_handler(lambda query: query.data.startswith('submit_homework'))
def submit_homework_callback(query: types.CallbackQuery):
    def get_content(message_content: types.Message):
        content = replace_special_characters(message_content.text)
        submission_status = submit_homework(student_id=student_id, topic=topic, content=content)
        if submission_status != 'success':
            bot.send_message(student_id, submission_status)
            return
        username = get_student_username(student_id=student_id)
        bot.send_message(
            MY_USER_ID,
            f'Користувач {username} подав домашнє завдання на розгляд.'
            f'\n\nДля перегляду зробленого д/з використайте /submitted_homework.'
        )
        bot.send_message(student_id, f'Домашнє завдання успішно подане на розгляд.')

    _, homework_id, student_id = query.data.split()
    homework_id, student_id = map(int, (homework_id, student_id))
    topic = get_topic(homework_id)
    sent_content = bot.send_message(student_id, 'Введіть зроблене завдання.')
    bot.register_next_step_handler(sent_content, get_content)
