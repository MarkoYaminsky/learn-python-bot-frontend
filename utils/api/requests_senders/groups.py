from utils.api.request_classes.query_parameter import QueryParameter
from utils.api.request_classes.request_type import RequestType
from utils.api.request_classes.graphql_request import GraphqlRequest


def create_group(group_name: str):
    request = GraphqlRequest.form_request(
        request_type=RequestType.MUTATION,
        instance_name='createGroup',
        query_params=[QueryParameter(parameter_name='groupName', parameter_value=group_name)],
    )
    request_details = GraphqlRequest(request).send_request()['requestDetails']
    return request_details


def add_student_to_group(student_name: str, group_name: str):
    request = GraphqlRequest.form_request(
        request_type=RequestType.MUTATION,
        instance_name='addStudentToGroup',
        query_params=[
            QueryParameter(
                parameter_name='groupName',
                parameter_value=group_name
            ),
            QueryParameter(
                parameter_name='studentUsername',
                parameter_value=student_name
            )
        ],
    )
    request_details = GraphqlRequest(request).send_request()['requestDetails']
    return request_details


def group_exists(group_name: str):
    request = GraphqlRequest.form_request(
        request_type=RequestType.QUERY,
        instance_name='group',
        query_params=[QueryParameter(parameter_name='name', parameter_value=group_name)],
        output_fields=['name']
    )
    response = GraphqlRequest(request).send_request()
    return bool(response)
