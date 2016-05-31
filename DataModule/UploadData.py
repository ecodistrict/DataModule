import json
import Abstract_Module

class UploadFromGeoJSON(Abstract_Module.AbstractModule):
    def __init__(self):
        self.status = ""
        self.valid_srs_list = ['urn:ogc:def:crs:OGC:1.3:CRS84']
        self._json_dict = {}
        self.insert_request = ""

    def upload_local_file(self, fileURL):
        with open(fileURL) as json_file:
            self._json_dict = json.load(json_file)

    def print_json(self):
        print self._json_dict

    def _create_insert_feature_request(self, properties, geometry):
        print geometry
        print properties

#        feature_name = _get_feature_name(properties)
#        feature_id = _get_or_create_feature_id(properties)

        for property_key, property_value in properties.iteritems():
            # todo: make those as insert request request somehow.
            print property_key
            print property_value
#
#         get properties in bldg table that match those of cityGML
#         add generic stuffs ? how ? why
#         req = """INSERT INTO bldg_building() """
#
# bldg_building(attr_gml_id, bldg_name, bldg_lod0footprint_value)
# SELECT
# attr_gml_id, bldg_name, bldg_lod0footprint_value
# FROM
# json_populate_record(null::bldg_building,
#                            '{
#                            "attr_gml_id":"Postpu 15A",
#                                          "bldg_name": "Postpu 15A",
#                                                       "bldg_lod0footprint_value": "POLYGON ((20.996672210356877 52.180446970412191 ,20.996437757122692 52.180452408787552 ,20.996364438184173 52.180440654790701 ,20.996266499534467 52.18043731357416 ,20.996176559053513 52.1804466648776 ,20.996099692189485 52.180461907147368 ,20.995879905881129 52.180471834800265 ,20.995883129932654 52.180492828493371 ,20.995861192766696 52.180494840998406 ,20.995812869890393 52.180524063326772 ,20.995668970177732 52.180529746774162 ,20.995645807184715 52.180513063883112 ,20.995613196705644 52.180513582924398 ,20.995611988004651 52.180505885249403 ,20.995548863061952 52.180508021844254 ,20.995559121400053 52.180627690714061 ,20.995540073961834 52.180628201779818 ,20.995544627079962 52.180670290276552 ,20.995793637527093 52.180661945706881 ,20.996684968634867 52.180632223886818 ,20.996685143016837 52.180616327122806 ,20.996797831996194 52.180613360505276 ,20.996849539871651 52.180580836449892 ,20.996846498534637 52.18054954484262 ,20.99700575823471 52.180545050510673 ,20.997002461414404 52.180478466478064 ,20.997030371448503 52.180469651612526 ,20.997039915902544 52.18045104980316 ,20.997030312496818 52.180432459463781 ,20.997000583772046 52.180426378548489 ,20.996780493330562 52.180432908772481 ,20.9967811267576 52.180455103731276 ,20.996671630275699 52.180458568321548 ,20.996672210356877 52.180446970412191 ))"
# }'
# );




def _check_srs(self):
        srs = self._json_dict.get('crs', None)
        if srs is None or srs not in self.valid_srs_list:
            self.status = "Failed - wrong srs. Only wgs84 is supported right now"
            return False
        else:
            return True

    """ Parse geometry and convert it as an insert request"""
    def _parse_geometry(self):
        ftype = self._json_dict.get('type', None)
        if ftype != 'FeatureCollection':
            self.status = "Failed - not feature collection in geoJSON"
            return False

        features_list = self._json_dict.get('features', [])
        for feature in features_list:
            properties = feature.get('properties', None)
            if properties is None:
                self.status += "Failed - At least one feature has no properties"
                return False

            geometry = feature.get('geometry', None)
            if geometry is None:
                self.status += "Failed - At least one feature has no geometry"
                return False

            # todo: assert geometry type srs ?
            _create_insert_feature_request(properties, geometry)
        return True

    def upload_buildings_geometry(self):
        if self._check_srs:
            self._parse_geometry()

        return self.status
