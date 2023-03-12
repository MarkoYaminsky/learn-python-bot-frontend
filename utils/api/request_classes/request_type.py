from enum import Enum


class RequestType(Enum):
    QUERY = 'query'
    MUTATION = 'mutation'
