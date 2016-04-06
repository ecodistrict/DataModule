class AbstractModule:
    def __init__(self, postresDataManager, schema_id):
        self.schemaID = schema_id
        self._pdm = postresDataManager
        self.responseData = {}

    def createSchemaRequest(self, request):
        return """  SET SCHEMA '{}';
                    {}""".format(self.schemaID, request)