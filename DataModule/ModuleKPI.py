import Abstract_Module


class ModuleKPI(Abstract_Module.AbstractModule):
    """
        class for saving and get complex kpi results
    """
    def save(self, kpi_id, kpi_value_list):
        for kpi in kpi_value_list:
            kpi_type = kpi.get('type', 'None')
            gml_id = kpi.get('gml_id', 'None')
            kpi_value = kpi.get('kpiValue', 'None')

            if kpi_type is 'None' or kpi_value is 'None' or gml_id is 'None':
                self._pdm.rollback_transactions()
                print "Failed - wrong json message"
                return "Failed - wrong json message"

            delete_request = self.create_schema_request("""DELETE FROM kpi_results WHERE kpi_type='{}'
                                         AND gml_id ='{}' AND kpi_id ='{}';""".format(kpi_type, gml_id, kpi_id))
            if self._pdm.execute_request(delete_request) == 'False':
                print "delete kpi failure : {}".format(delete_request)
                self._pdm.rollback_transactions()
                return "Failed - Can't delete previous results"

            insert_request = self.create_schema_request("""INSERT INTO kpi_results (kpi_type, kpi_id, gml_id, kpi_value)
                                         VALUES ('{}', '{}', '{}', {})""".format(kpi_type, kpi_id, gml_id, kpi_value))
            if self._pdm.execute_request(insert_request) == 'False':
                print "insert kpi failure : {}".format(insert_request)
                self._pdm.rollback_transactions()
                return "Failed - Can't delete insert results"

        self._pdm.commit_transactions()
        return "success - data added to the database"

    def load(self, kpi_id):
        request = self.create_schema_request("""SELECT id, kpi_id, gml_id, kpi_value, kpi_type FROM kpi_results
                                              WHERE kpi_id='{}';""".format(kpi_id))

        results = self._pdm.get_data_list_values(request)
        for res in results:
            print res

    def _create_geojson_request(self, table_name, table_geometry_attribute):
        return """SET SCHEMA 'public';
                 SELECT row_to_json(fc) FROM(SELECT 'FeatureCollection' As type, array_to_json(array_agg(f)) As features
                 FROM(SELECT 'Feature' As type, ST_AsGeoJSON(ST_FlipCoordinates({}))::json As geometry,
                      row_to_json((SELECT l FROM(SELECT attr_gml_id AS gml_id) As l)) As properties FROM
                         {}.{} As lg   ) As f )  As fc;""".format(table_geometry_attribute, self.schemaID, table_name)

    def get_geojson(self, element_filter):
        if element_filter == 'building':
            request = self._create_geojson_request("bldg_building", "bldg_lod0footprint_value")
            return self._pdm.get_data_value(request, None)

        else:
            return ''
