class QueryParameter:
    def __init__(self, parameter_name: str, parameter_value: int | str | bool):
        self.parameter_name = parameter_name
        self.parameter_value = parameter_value

    def __str__(self):
        return '{' + f"{self.parameter_name}: {self.parameter_value}" + '}'
