from typing import Any

from telebot import types


def assign_homework_keyboard():
    markup = types.InlineKeyboardMarkup()
    group_option = types.InlineKeyboardButton("Групі", callback_data="assign_to_group")
    personal_option = types.InlineKeyboardButton(
        "Студенту", callback_data="assign_to_student"
    )
    markup.row(group_option, personal_option)
    return markup


def submitted_homework_keyboard(student_id: int, homework_id: int):
    approve_option = types.InlineKeyboardButton(
        "Прийняти", callback_data=f"approve {student_id} {homework_id}"
    )
    decline_option = types.InlineKeyboardButton(
        "Відхилити", callback_data=f"decline {student_id} {homework_id}"
    )
    markup = types.InlineKeyboardMarkup()
    markup.row(approve_option, decline_option)
    return markup


def submit_homework_keyboard(homework: list[dict[str, Any]], student_id: int):
    markup = types.InlineKeyboardMarkup()
    for homework in homework:
        homework_option = types.InlineKeyboardButton(
            homework["topic"],
            callback_data=f'submit_homework {homework["id"]} {student_id}',
        )
        markup.row(homework_option)
    return markup


def remind_students_keyboard(self_id: int):
    markup = types.InlineKeyboardMarkup()
    group_option = types.InlineKeyboardButton(
        "Групі", callback_data=f"remind_group_{self_id}"
    )
    personal_option = types.InlineKeyboardButton(
        "Всім", callback_data=f"remind_everybody_{self_id}"
    )
    markup.row(group_option, personal_option)
    return markup


def homework_keyboard(homework_id: int, student_id: int):
    markup = types.InlineKeyboardMarkup()
    submit_homework_button = types.InlineKeyboardButton(
        "Подати завдання на розгляд",
        callback_data=f"submit_homework {homework_id} {student_id}",
    )
    markup.row(submit_homework_button)
    return markup
