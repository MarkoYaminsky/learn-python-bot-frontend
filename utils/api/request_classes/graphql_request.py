import requests

from settings.config import SERVER_URL
from utils.api.request_classes.output_field import OutputField
from utils.api.request_classes.query_parameter import QueryParameter
from utils.api.request_classes.request_type import RequestType


class GraphqlRequest:
    def __init__(self, query):
        self.query = query

    @property
    def query_name(self):
        line_with_request_name = self.query.split()[2]
        request_is_parametrized = '(' in line_with_request_name
        return line_with_request_name.split('(' if request_is_parametrized else '{')[0].strip()

    @staticmethod
    def __format_query_parameters(query_params: list[QueryParameter]) -> str:
        for query_param in query_params:
            if isinstance(query_param.parameter_value, str):
                query_param.parameter_value = f'"{query_param.parameter_value}"'

        formatted_query_params = ", ".join([f"{query_param.parameter_name}: {query_param.parameter_value}" for query_param in query_params])
        return formatted_query_params

    @classmethod
    def form_request(
            cls,
            request_type: RequestType,
            instance_name: str,
            query_params: list[QueryParameter] = None,
            output_fields: list[str | OutputField] = None
    ):
        output_fields = ' '.join([
            field if isinstance(field, str)
            else f"{field.parrent_name} " + '{' + f" {' '.join(field.nested_fields)} " + '}'
            for field in output_fields
        ]) if output_fields else 'requestDetails'
        params = cls.__format_query_parameters(query_params) if query_params else None
        query_arguments = f'({params})' if query_params else ''
        request = request_type.value + ' { ' + f'{instance_name}' + query_arguments + ' { ' + output_fields + ' } }'
        return request

    def send_request(self):
        return requests.post(SERVER_URL, json={'query': self.query}).json()['data'][self.query_name]
