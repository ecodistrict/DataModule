
class Module_LCA:
    """
        class for getting LCA data
    """
    def __init__(self, postresDataManager, schema_id):
        self.schemaID = schema_id
        self._pdm = postresDataManager
        self.responseData = {}

    def getData(self):
        return self.responseData

class Module_LCC:
    """
        class for getting LCC data
    """
    def __init__(self, postresDataManager, schema_id):
        self.schemaID = schema_id
        self._pdm = postresDataManager
        self.responseData = {}

    def _getBuildingsData(self):
        request ="""SELECT attr_gml_id FROM {}.bldg_building;""".format(self.schemaID)
        bldg_id_list =  self._pdm.get(request)

    def getData(self):
        self.responseData['Buildings'] = self._getBuildingsData()

        return self.responseData