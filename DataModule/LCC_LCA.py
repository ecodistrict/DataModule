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

            building_data['gml_id'] = gml_id
            building_list.append(building_data)
        return building_list

    def _getDistrictData(self):
        request_double_attr = self.createSchemaRequest(
            """SELECT DISTINCT attr_name FROM luse_landuse_gen_doubleattribute;""")
        district_attr_double_list = [i[0] for i in self._pdm.getDataListValues(request_double_attr)]

        request_int_attr = self.createSchemaRequest(
            """SELECT DISTINCT attr_name FROM luse_landuse_gen_intattribute;""")
        district_attr_int_list = [i[0] for i in self._pdm.getDataListValues(request_int_attr)]

        district_data = {}
        for attr in district_attr_double_list:
            request_double = self.createSchemaRequest("""SELECT gen_value FROM luse_landuse_gen_doubleattribute
                  WHERE attr_name='{}';""").format(attr)
            district_data[attr] = self._pdm.getDataValue(request_double, float)

        for attr in district_attr_int_list:
            request_int = self.createSchemaRequest("""SELECT gen_value FROM luse_landuse_gen_intattribute
                      WHERE attr_name='{}';""").format(attr)
            district_data[attr] = self._pdm.getDataValue(request_int, int)

        return district_data

    def getData(self):
        self.responseData['Buildings'] = self._getBuildingsData()
        self.responseData['District'] = self._getDistrictData()
        print self.responseData
        return self.responseData