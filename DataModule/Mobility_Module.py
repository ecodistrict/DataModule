import Abstract_Module

class Module_Mobility(Abstract_Module.AbstractModule):
    """
        class for getting LCC data
    """

    def _getDistrictData(self):
        request_double_attr = self.createSchemaRequest(
            """SELECT DISTINCT attr_name FROM tran_transportationcomplex_gen_doubleattribute;""")
        district_attr_double_list = [i[0] for i in self._pdm.getDataListValues(request_double_attr)]

        district_data = {}
        for attr in district_attr_double_list:
            request_double = self.createSchemaRequest("""SELECT gen_value FROM tran_transportationcomplex_gen_doubleattribute
                  WHERE attr_name='{}';""").format(attr)
            district_data[attr] = self._pdm.getDataValue(request_double, float)

        return district_data

    def getData(self):
        self.responseData['District'] = self._getDistrictData()
        print self.responseData
        return self.responseData