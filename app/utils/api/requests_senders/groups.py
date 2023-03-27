import pandas as pd

from app.utils.api.request_classes.graphql_request import GraphqlRequest
from app.utils.api.request_classes.output_field import OutputField
from app.utils.api.request_classes.query_parameter import QueryParameter
from app.utils.api.request_classes.request_type import RequestType


def create_group(group_name: str):
    request = GraphqlRequest.form_request(
        request_type=RequestType.MUTATION,
        instance_name="createGroup",
        query_params=[
            QueryParameter(parameter_name="groupName", parameter_value=group_name)
        ],
    )
    request_details = GraphqlRequest(request).send_request().get("requestDetails", None)
    return request_details


def add_student_to_group(student_name: str, group_name: str):
    request = GraphqlRequest.form_request(
        request_type=RequestType.MUTATION,
        instance_name="addStudentToGroup",
        query_params=[
            QueryParameter(parameter_name="groupName", parameter_value=group_name),
            QueryParameter(
                parameter_name="studentUsername", parameter_value=student_name
            ),
        ],
    )
    request_details = GraphqlRequest(request).send_request().get("requestDetails", None)
    return request_details


def group_exists(group_name: str):
    request = GraphqlRequest.form_request(
        request_type=RequestType.QUERY,
        instance_name="group",
        query_params=[
            QueryParameter(parameter_name="name", parameter_value=group_name)
        ],
        output_fields=["name"],
    )
    response = GraphqlRequest(request).send_request()
    return bool(response)


def get_undone_homework_by_group(group_name: str):
    request = GraphqlRequest.form_request(
        request_type=RequestType.QUERY,
        instance_name="undoneHomeworkByGroup",
        query_params=[
            QueryParameter(parameter_name="groupName", parameter_value=group_name)
        ],
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
