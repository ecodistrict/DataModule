import json
import os

import Abstract_Module


class UploadFromGeoJSON(Abstract_Module.AbstractModule):
    def __init__(self):
        self.status = ""
        self.valid_srs_list = ['urn:ogc:def:crs:OGC:1.3:CRS84']
        self.valid_gml_type = {'BUILDINGS':'bldg_building', }
        self.gml_table = ''
        self._json_dict = {}
        self.insert_request = ""

    def upload_data(self, filename):
        self._load_json_data(filename)

        if not self._json_dict:
            self.status += "Can't convert data into right json format"
        else:
            self._parse_properties()

        return self.status

    def _load_json_data(self, fileURL):
        with open(fileURL, "r") as file_data:
            file_name, file_extension = os.path.splitext(fileURL)
            if file_extension.upper() == ".JSON":
                self._json_dict = json.load(file_data)

    def print_json(self):
        print self._json_dict

    def _create_insert_feature_request(self, properties):
        print properties

        feature_id = properties.get('FID_1', None)
        if not feature_id:
            self.status = "Failed - no FID_1"
            return False

        if not self._execute_delete_request(feature_id, 'gen_intattribute'):
            return False
        if not self._execute_delete_request(feature_id, 'gen_doubleattribute'):
            return False
        if not self._execute_delete_request(feature_id, 'gen_stringattribute'):
            return False

        for property_key, property_value in properties.iteritems():
            if property_value.isdigit():
                if not self._execute_insert_request(feature_id, property_key, property_value, 'gen_intattribute'):
                    return False
            elif property_value.isdecimal():
                if not self._execute_insert_request(feature_id, property_key, property_value, 'gen_doubleattribute'):
                    return False
            else:
                if not self._execute_insert_request(feature_id, property_key, property_value, 'gen_stringattribute'):
                    return False

        self._pdm.commit_transactions()

    def _execute_delete_requests(self, gml_id, extension):
        delete_request = self.create_schema_request("""DELETE FROM {}_{} WHERE parentfk='{}'; """
                                                    .format(self.gml_table, extension, gml_id,))

        if self._pdm.execute_request(delete_request) == 'False':
            print "delete attribute failure : {}".format(delete_request)
            self._pdm.rollback_transactions()
            self.status = "Failed - Can't delete previous data"
            return False
        return True

    def _execute_insert_request(self, gml_id, key, value, extension):
        insert_request = self.create_schema_request("""INSERT INTO {}_{} (parentfk, num, attr_name, gen_value) VALUES ('{}','0','{}','{}'); """
            .format(self.gml_table, extension, gml_id, key, value)

        if self._pdm.execute_request(insert_request) == 'False':
            print "insert attribute failure : {}".format(insert_request)
            self._pdm.rollback_transactions()
            self.status = "Failed - Can't delete insert results"
            return False
        return True

    def _check_srs(self):
        return True
#         srs = self._json_dict.get('crs', None)
#         if srs is None or srs not in self.valid_srs_list:
#             self.status = "Failed - wrong srs. Only wgs84 is supported right now"
#             return False
#         else:
#             return True

    """ Parse properties and convert it as an insert request"""
    def _parse_properties(self):
        ftype = self._json_dict.get('type', None)
        if ftype != 'FeatureCollection':
            self.status = "Failed - not feature collection in geoJSON"
            return False

        gml_type = self._json_dict.get('gml_type', None)
        if not gml_type:
            self.status = "Failed - not gml type defined in geoJSON"
            return False

        self.gml_table = self.valid_gml_type.get(gml_type.upper(), None)
        if not self.gml_table:
            self.status = "Failed - gml type is not a valid one"
            return False

        features_list = self._json_dict.get('features', [])
        for feature in features_list:
            properties = feature.get('properties', None)
            if properties is None:
                self.status += "Failed - At least one feature has no properties"
                return False

            self._create_insert_feature_request(properties)
        return True


