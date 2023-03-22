class OutputField:
    def __init__(self, parrent_name: str, nested_fields: list[str]):
        self.parrent_name = parrent_name
        self.nested_fields = nested_fields

    def __str__(self):
        return "{" + f"{self.parrent_name}: {self.nested_fields}" + "}"
