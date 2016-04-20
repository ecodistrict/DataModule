import Abstract_Module


class ModuleMobility(Abstract_Module.AbstractModule):
    """
        class for getting LCC data
    """
    def _get_district_data(self):
        request_double_attr = self.create_schema_request(
            """SELECT DISTINCT attr_name FROM tran_transportationcomplex_gen_doubleattribute;""")
        district_attr_double_list = [i[0] for i in self._pdm.get_data_list_values(request_double_attr)]

        district_data = {}
        for attr in district_attr_double_list:
            request_double = self.create_schema_request("""SELECT gen_value FROM tran_transportationcomplex_gen_doubleattribute
                  WHERE attr_name='{}';""").format(attr)
            district_data[attr] = self._pdm.get_data_value(request_double, float)

        return district_data

    def get_data(self):
        self.responseData['District'] = self._get_district_data()
        print self.responseData
        return self.responseData
