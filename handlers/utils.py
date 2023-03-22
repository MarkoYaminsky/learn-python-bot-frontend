import time

from telebot import types

from settings.bot import bot
from utils.api.requests_senders.groups import group_exists, get_undone_homework_by_group
from utils.api.requests_senders.homework import assign_homework
from utils.api.requests_senders.students import (
    get_student_id,
    get_students_by_group_name,
    get_students_with_undone_homework,
)


def assignment_with_option(option: str, from_user_id: int):
    def get_user_or_group(user_or_group_message: types.Message):
        user_or_group = user_or_group_message.text
        option_form = "Групи" if option == "group" else "Студента"

        if (
            option == "group"
            and not group_exists(user_or_group)
            or option == "student"
            and not get_student_id(user_or_group)
        ):
            bot.send_message(
                from_user_id, f"{option_form} з назвою {user_or_group} не існує."
            )
            return

        sent_topic = bot.send_message(from_user_id, "Введіть тему домашнього завдання.")
        bot.register_next_step_handler(sent_topic, get_topic, user_or_group)

    def get_topic(topic_message: types.Message, user_or_group):
        topic = topic_message.text
        assignment_details = assign_homework(
            option=query_params[option], option_value=user_or_group, topic=topic
        )
        if assignment_details != "success":
            bot.send_message(from_user_id, assignment_details)
            return

        after_assignment_phrase = (
            ""
            f'Ви отримали нове домашнє завдання з теми "{topic}". Щоб переглянути його, використайте /homework'
        )

        if option == "group":
            for student in get_students_by_group_name(user_or_group):
                student_id = student["id"]
                bot.send_message(student_id, after_assignment_phrase)
        else:
            bot.send_message(get_student_id(user_or_group), after_assignment_phrase)

        option_form = "студентові" if option == "student" else "групі"
        bot.send_message(
            from_user_id,
            f'Успішно призначено домашнє завдання з теми "{topic}" {option_form} {user_or_group}.',
        )

    query_params = {"group": "groupName", "student": "studentUsername"}

    destination = "групу, якій" if option == "group" else "псевдонім студента, якому"
    sent_user_or_group = bot.send_message(
        from_user_id, f"Введіть {destination} хочете призначити домашнє завдання."
    )
    bot.register_next_step_handler(sent_user_or_group, get_user_or_group)


def replace_special_characters(string: str):
    return (
        string.replace("\r\n", "%%")
        .replace("\n", "%%")
        .replace("\r", "%%")
        .replace('"', "'")
        .replace("    ", "\t")
        .replace("\\", "##")
        .strip()
    )


def group_tasks_by_username(data: list[dict[str, str]]):
    items = {}
    for item in data:
        student = item["username"]
        task = item["topic"]
        if student not in items:
            items.update({student: [task]})
        else:
            items[student].append(task)
    return items


def remind_by_option(option: str, self_id: int):
    if option == "group":

        def get_group_name(group_name_message: types.Message):
            nonlocal group_name
            group_name = group_name_message.text

        group_name: str = ""
        sent_group_name = bot.send_message(self_id, "Введіть назву групи.")
        bot.register_next_step_handler(sent_group_name, get_group_name)

        while not group_name:
            time.sleep(0.1)
        return get_undone_homework_by_group(group_name)

    elif option == "everybody":
        return get_students_with_undone_homework()
