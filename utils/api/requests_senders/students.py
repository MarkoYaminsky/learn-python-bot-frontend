import pandas as pd

from utils.api.request_classes.output_field import OutputField
from utils.api.request_classes.query_parameter import QueryParameter
from utils.api.request_classes.request_type import RequestType
from utils.api.request_classes.graphql_request import GraphqlRequest
from utils.decorators import logged


def get_students_by_group_name(group_name: str):
    request = GraphqlRequest.form_request(
        request_type=RequestType.QUERY,
        instance_name="students",
        query_params=[
            QueryParameter(parameter_name="groupName", parameter_value=group_name)
        ],
        output_fields=["username", "telegramId"],
    )
    data = GraphqlRequest(request).send_request()
    df_values = pd.DataFrame(data).values
    return [
        {"username": username, "id": telegram_id} for username, telegram_id in df_values
    ]


def get_students_with_undone_homework():
    request = GraphqlRequest.form_request(
        request_type=RequestType.QUERY,
        instance_name="studentsWithUndoneHomework",
        output_fields=[
            OutputField(parrent_name="student", nested_fields=["username"]),
            OutputField(parrent_name="homework", nested_fields=["topic"]),
        ],
    )
    data = GraphqlRequest(request).send_request()
    df_values = pd.DataFrame(data).values
    return [
        {"username": username["username"], "topic": topic["topic"]}
        for username, topic in df_values
    ]


def get_student_username(student_id: int):
    request = GraphqlRequest.form_request(
        request_type=RequestType.QUERY,
        instance_name="student",
        query_params=[
            QueryParameter(parameter_name="telegramId", parameter_value=student_id)
        ],
        output_fields=["username"],
    )
    response = GraphqlRequest(request).send_request()
    return response["username"] if response else None


def get_student_id(username: str):
    request = GraphqlRequest.form_request(
        request_type=RequestType.QUERY,
        instance_name="student",
        query_params=[
            QueryParameter(parameter_name="username", parameter_value=username)
        ],
        output_fields=["telegramId"],
    )
    response = GraphqlRequest(request).send_request()
    return response["telegramId"] if response else None


def get_student_group(student_id: int):
    request = GraphqlRequest.form_request(
        request_type=RequestType.QUERY,
        instance_name="student",
        query_params=[
            QueryParameter(parameter_name="telegramId", parameter_value=student_id)
        ],
        output_fields=[OutputField(parrent_name="group", nested_fields=["name"])],
    )
    response = GraphqlRequest(request).send_request()
    group = response["group"]
    return group["name"] if group else None


@logged
def register_student(telegram_id: int, username: str):
    request = GraphqlRequest.form_request(
        request_type=RequestType.MUTATION,
        instance_name="registerStudent",
        query_params=[
            QueryParameter(parameter_name="telegramId", parameter_value=telegram_id),
            QueryParameter(parameter_name="username", parameter_value=username),
        ],
    )
    request_details = GraphqlRequest(request).send_request()["requestDetails"]
    return request_details


@logged
def update_student(telegram_id: int, username: str):
    request = GraphqlRequest.form_request(
        request_type=RequestType.MUTATION,
        instance_name="updateStudent",
        query_params=[
            QueryParameter(parameter_name="telegramId", parameter_value=telegram_id),
            QueryParameter(parameter_name="username", parameter_value=username),
        ],
    )
    request_details = GraphqlRequest(request).send_request().get("requestDetails", None)
    return request_details
