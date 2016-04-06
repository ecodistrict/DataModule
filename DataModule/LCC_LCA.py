import Abstract_Module

class Module_LCA(Abstract_Module.AbstractModule):
    """
        class for getting LCA data
    """
    def __init__(self, postresDataManager, schema_id):
        self.schemaID = schema_id
        self._pdm = postresDataManager
        self.responseData = {}

    def getData(self):
        return self.responseData

class Module_LCC(Abstract_Module.AbstractModule):
    """
        class for getting LCC data
    """

    def _getBuildingsData(self):
        request = self.createSchemaRequest("""SELECT attr_gml_id FROM bldg_building;""")
        bldg_id_list = self._pdm.getDataListValues(request)
        for a in bldg_id_list:
            request2 = """ """

    def getData(self):
        self.responseData['Buildings'] = self._getBuildingsData()

        return self.responseData