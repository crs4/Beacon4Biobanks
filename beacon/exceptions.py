from aiohttp.web_exceptions import HTTPNotFound


class OperationNotSupported(HTTPNotFound):
    def __init__(self):
        super().__init__(text="This beacon doesn't support this operation")

class SchemaNotSupported(Exception):
    def __init__(self, entry_type, schema_name):
        super().__init__(f"The schema with name {schema_name} is not specified for entry type {entry_type}")


class DefaultSchemaNotSpecified(Exception):
    pass
