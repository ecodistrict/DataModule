import json
import os

import Abstract_Module
import DataModule.DataManager as DataManager


class UploadModule(Abstract_Module.AbstractModule):
    def __init__(self):
        self.prefix = 'trout_'
        pdm = DataManager.PostgresDataManager()
        pdm.connect("vps17642.public.cloudvps.com", "Warsaw", "postgres", "x0mxaJc69J9KAlFNsaDt", "5443")
        Abstract_Module.AbstractModule.__init__(self, pdm, "")
        self.status = ""
        self.valid_srs_list = ['urn:ogc:def:crs:OGC:1.3:CRS84']
        self.valid_gml_type = {'BUILDINGS':'Ecodistrict_building', }
        self.gml_table = ''
        self._json_dict = {}
        self.insert_request = ""

    def upload_data(self, filename):
        self._load_json_data(filename)
        if not self._json_dict:
            self.status += "Can't convert data into right json format"
        else:
            if self._check_case_variant():
                self._parse_features()

        return self.status

    def _check_case_variant(self):
        case_id = self._json_dict.get('caseId', 'null')
        variant_id = self._json_dict.get('variantId', 'null')
        base_schema_id = case_id if variant_id is 'null' or variant_id is None else case_id + "_" + variant_id
        self.schemaID = self.prefix + base_schema_id
        if not self._pdm.check_if_schema_exists(self.schemaID):
            self.status += "Failed - schema for case and variant doesn't exist"
            return False
        return True

    def _load_json_data(self, fileURL):
        with open(fileURL, "r") as file_data:
            file_name, file_extension = os.path.splitext(fileURL)
            if file_extension.upper() == ".JSON":
                self._json_dict = json.load(file_data)

    def print_json(self):
        print self._json_dict

    def _create_feature_if_necessary(self, feature_id):
        req = self.create_schema_request("""INSERT INTO {} (fid) VALUES ('{}'); """.format(self.gml_table, feature_id))
        self._pdm.execute_request(req)
        self._pdm.commit_transactions()

    def _create_insert_feature_request(self, properties, feature_id):
        self._create_feature_if_necessary(feature_id)
        if not self._update_feature(feature_id, properties):
            return False
        return True

    def _update_feature(self, gml_id, properties):
        req = "UPDATE {} SET ".format(self.gml_table)
        firstPass = True
        for property_key, property_value in properties.iteritems():
            if property_key != 'FID':
                if not firstPass:
                    req += ", "
                else:
                    firstPass = False
                req += "{}='{}'".format(property_key, property_value)

        req += " WHERE FID='{}';".format(gml_id)
        embedded_req = self.create_schema_request(req)

        if not self._pdm.execute_request(embedded_req):
            self.status = "Failed - can't update element"
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
    def _parse_features(self):
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
                self.status += "Failed - At least one feature has no properties (at least FID is mandatory)"
                return False

            feature_id = properties.get('FID', None)
            if not feature_id:
                self.status = "Failed - no FID"
                return False

            if not self._create_insert_feature_request(properties, feature_id):
                self.status = "Failed - can't update feature"
                self._pdm.rollback_transactions()
                return False

            geometry = feature.get('geometry', None)
            if geometry is not None:
                if not self._update_feature_geometry( json.dumps(geometry), feature_id):
                    self.status = "Failed - can't upload geometry"
                    self._pdm.rollback_transactions()
                    return False

            self._pdm.commit_transactions()

        return True

    def _update_feature_geometry(self, geometry, feature_id):
        based_req = """UPDATE {}.{} SET lod0footprint=( ST_AsText(ST_GeomFromGeoJSON('{}') ) ) WHERE FID='{}';"""\
            .format(self.schemaID, self.gml_table, geometry, feature_id)

        geom_req = """ SET SCHEMA 'public';  {}""".format(based_req)

        if not self._pdm.execute_request(geom_req):
            self.status = "Failed - can't update geometry element"
            return False

        return True
