import Abstract_Module
import json


class ModuleMobility(Abstract_Module.AbstractModule):
    """
        class for getting LCC data
    """
    def _get_district_data(self):
        request_double_attr = self.create_schema_request(
            """SELECT DISTINCT attr_name FROM tran_trafficarea_gen_doubleattribute;""")
        district_attr_double_list = [i[0] for i in self._pdm.get_data_list_values(request_double_attr)]

        request_string_attr = self.create_schema_request(
            """SELECT DISTINCT attr_name FROM tran_trafficarea_gen_stringattribute;""")
        district_attr_string_list = [i[0] for i in self._pdm.get_data_list_values(request_string_attr)]

        district_data = {}
        for attr in district_attr_double_list:
            request_double = self.create_schema_request("""SELECT gen_value FROM tran_trafficarea_gen_doubleattribute
                  WHERE attr_name='{}';""").format(attr)
            district_data[attr] = self._pdm.get_data_value(request_double, float)

        for attr in district_attr_string_list:
            request_string = self.create_schema_request("""SELECT gen_value FROM tran_trafficarea_gen_stringattribute
                  WHERE attr_name='{}';""").format(attr)
            district_data[attr] = self._pdm.get_data_value(request_string, str)

        return district_data

    def get_data(self):
        self.responseData['District'] = self._get_district_data()
        print self.responseData
        return self.responseData
