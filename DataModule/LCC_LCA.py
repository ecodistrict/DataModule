
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
        request ="""SELECT * FROM {}.bldg_building bldg
	      JOIN {}.bldg_building_gen_intattribute bldg_int ON bldg_int.parentfk = bldg.attr_gml_id
	      JOIN {}.bldg_building_gen_doubleattribute bldg_dble ON bldg_dble.parentfk = bldg.attr_gml_id
	      JOIN {}.bldg_building_gen_stringattribute bldg_str ON bldg_str.parentfk = bldg.attr_gml_id
	      """.format(self.schemaID, self.schemaID, self.schemaID, self.schemaID)
        return self._pdm.getJsonifyValue(request)

    def getData(self):
        self.responseData['Buildings'] = self._getBuildingsData()

        return self.responseData