import Abstract_Module

class Module_LCC_LCA(Abstract_Module.AbstractModule):
    """
        class for getting LCC data
    """
    def _getBuildingStringAttribute(self, attr_type, bldg_id):
        request = self.createSchemaRequest("""SELECT string_attribute.gen_value FROM bldg_building
                        JOIN bldg_building_gen_stringattribute string_attribute ON bldg_building.attr_gml_id = string_attribute.parentfk
                        WHERE string_attribute.attr_name = '{}' AND bldg_building.attr_gml_id='{}'
                        """.format(attr_type, bldg_id))
        return self._pdm.getDataValue(request, str)

    def _getBuildingDoubleAttribute(self, attr_type, bldg_id):
        request = self.createSchemaRequest("""SELECT double_attribute.gen_value FROM bldg_building
                        JOIN bldg_building_gen_doubleattribute double_attribute ON bldg_building.attr_gml_id = double_attribute.parentfk
                        WHERE double_attribute.attr_name = '{}' AND bldg_building.attr_gml_id='{}'
                        """.format(attr_type, bldg_id))
        return self._pdm.getDataValue(request, float)

    def _getBuildingIntAttribute(self, attr_type, bldg_id):
        request = self.createSchemaRequest("""SELECT int_attribute.gen_value FROM bldg_building
                        JOIN bldg_building_gen_intattribute int_attribute ON bldg_building.attr_gml_id = int_attribute.parentfk
                        WHERE int_attribute.attr_name = '{}' AND bldg_building.attr_gml_id='{}'
                        """.format(attr_type, bldg_id))
        return self._pdm.getDataValue(request, int)


    def _getBuildingsData(self):
        request_str_attr = self.createSchemaRequest("""SELECT DISTINCT attr_name FROM bldg_building_gen_stringattribute;""")
        bldg_attr_string_list = [i[0] for i in self._pdm.getDataListValues(request_str_attr)]

        request_double_attr = self.createSchemaRequest("""SELECT DISTINCT attr_name FROM bldg_building_gen_doubleattribute;""")
        bldg_attr_double_list = [i[0] for i in self._pdm.getDataListValues(request_double_attr)]

        request_int_attr = self.createSchemaRequest("""SELECT DISTINCT attr_name FROM bldg_building_gen_intattribute;""")
        bldg_attr_int_list = [i[0] for i in self._pdm.getDataListValues(request_int_attr)]

        request_bldg_ids = self.createSchemaRequest("""SELECT attr_gml_id FROM bldg_building;""")
        bldg_id_list = [i[0] for i in self._pdm.getDataListValues(request_bldg_ids)]

        building_list = []
        for gml_id in bldg_id_list:
            building_data = {}
            for attr in bldg_attr_string_list:
                building_data[attr] = self._getBuildingStringAttribute(attr, gml_id)

            for attr in bldg_attr_double_list:
                building_data[attr] = self._getBuildingDoubleAttribute(attr, gml_id)

            for attr in bldg_attr_int_list:
                building_data[attr] = self._getBuildingIntAttribute(attr, gml_id)

            building_data['id'] = gml_id
            building_list.append(building_data)
        return building_list

    def getData(self):
        self.responseData['Buildings'] = self._getBuildingsData()
        print self.responseData
        return self.responseData