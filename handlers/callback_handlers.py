from telebot import types

from settings.bot import bot
from handlers.utils import assignment_with_option
from utils.api.requests_senders.homework import approve_or_decline_homework, get_topic


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
