import pandas as pd

from utils.api.request_classes.output_field import OutputField
from utils.api.request_classes.query_parameter import QueryParameter
from utils.api.request_classes.request_type import RequestType
from utils.api.request_classes.graphql_request import GraphqlRequest


def homework_exists(topic: str):
    request = GraphqlRequest.form_request(
        request_type=RequestType.QUERY,
        instance_name='homeworkInstance',
        query_params=[QueryParameter(parameter_name='topic', parameter_value=topic)],
        output_fields=['topic']
    )
    data = GraphqlRequest(request).send_request()
    return bool(data)


def get_homework(telegram_id: int):
    request = GraphqlRequest.form_request(
        request_type=RequestType.QUERY,
        instance_name='homework',
        query_params=[QueryParameter(parameter_name='telegramId', parameter_value=telegram_id)],
        output_fields=['topic', 'task', 'deadline', 'id']
    )
    data = GraphqlRequest(request).send_request()
    return [
        {
            'topic': homework['topic'],
            'task': homework['task'],
            'deadline': homework['deadline'],
            'id': homework['id']
        }
        for homework in data
    ]


def submit_homework(student_id: int, topic: str, content: str):
    request = GraphqlRequest.form_request(
        request_type=RequestType.MUTATION,
        instance_name='submitHomework',
        query_params=[
            QueryParameter(
                parameter_name='studentId',
                parameter_value=student_id
            ),
            QueryParameter(
                parameter_name='topic',
                parameter_value=topic
            ),
            QueryParameter(
                parameter_name='content',
                parameter_value=content
            )
        ]
    )
    request_details = GraphqlRequest(request).send_request()['requestDetails']
    return request_details


def add_homework(topic: str, task: str):
    request = GraphqlRequest.form_request(
        request_type=RequestType.MUTATION,
        instance_name='createHomework',
        query_params=[
            QueryParameter(
                parameter_name='topic',
                parameter_value=topic
            ),
            QueryParameter(
                parameter_name='task',
                parameter_value=task
            )
        ]
    )
    request_details = GraphqlRequest(request).send_request()['requestDetails']
    return request_details


def assign_homework(option: str, option_value: str, topic: str):
    request = GraphqlRequest.form_request(
        request_type=RequestType.MUTATION,
        instance_name='assignHomework',
        query_params=[
            QueryParameter(
                parameter_name=option,
                parameter_value=option_value
            ),
            QueryParameter(
                parameter_name='homeworkTopic',
                parameter_value=topic
            )
        ]
    )
    request_details = GraphqlRequest(request).send_request()['requestDetails']
    return request_details


def get_submitted_homework():
    request = GraphqlRequest.form_request(
        request_type=RequestType.QUERY,
        instance_name='submittedHomework',
        output_fields=[
            'content',
            OutputField(
                parrent_name='student',
                nested_fields=['telegramId', 'username']
            ),
            OutputField(
                parrent_name='homework',
                nested_fields=['id', 'task']
            )
        ]
    )
    data = GraphqlRequest(request).send_request()
    df_values = pd.DataFrame(data).values
    return [{'content': content, 'student': student, 'homework': homework} for content, student, homework in df_values]


def approve_or_decline_homework(option: str, student_id: int, homework_id: int):
    query_option = {'approve': 'markHomeworkAsDone', 'decline': 'declineHomework'}
    request = GraphqlRequest.form_request(
        request_type=RequestType.MUTATION,
        instance_name=query_option[option],
        query_params=[
            QueryParameter(
                parameter_name='studentId',
                parameter_value=student_id),
            QueryParameter(
                parameter_name='homeworkId',
                parameter_value=homework_id)
        ]
    )
    GraphqlRequest(request).send_request()


def get_topics():
    request = GraphqlRequest.form_request(
        request_type=RequestType.QUERY,
        instance_name='homework',
        output_fields=['topic']
    )
    data = GraphqlRequest(request).send_request()
    return [homework['topic'] for homework in data]


def get_topic(homework_id: int):
    query = GraphqlRequest.form_request(
        request_type=RequestType.QUERY,
        instance_name="homeworkInstance",
        query_params=[QueryParameter(parameter_name="homeworkId", parameter_value=homework_id)],
        output_fields=['topic']
    )
    data = GraphqlRequest(query).send_request()
    return data['topic']
