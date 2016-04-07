import Abstract_Module

class Module_KPI(Abstract_Module.AbstractModule):
    """
        class for saving and get complex kpi results
    """
    def save(self, kpi_id, kpiValueList):
        for kpi in kpiValueList:
            kpi_type = kpi.get('type', 'None')
            gml_id = kpi.get('gml_id', 'None')
            kpi_value = kpi.get('kpiValue', 'None')

            if kpi_type=='None' or kpi_value=='None' or gml_id=='None':
                self._pdm.rolleback_transactions()
                print "Failed - wrong json message"
                return "Failed - wrong json message"

            delete_request = self.createSchemaRequest("""DELETE FROM kpi_results WHERE kpi_type='{}'
                                                          AND gml_id ='{}' AND kpi_id ='{}';""".format(kpi_type, gml_id, kpi_id))
            if self._pdm.executeRequest(delete_request) == 'False':
                print "delete kpi failure : {}".format(delete_request)
                self._pdm.rolleback_transactions()
                return "Failed - Can't delete previous results"

            insert_Request = self.createSchemaRequest("""INSERT INTO kpi_results (kpi_type, kpi_id, gml_id, kpi_value)
                                                          VALUES ('{}', '{}', '{}', {})""".format(kpi_type, kpi_id, gml_id, kpi_value) )
            if self._pdm.executeRequest(insert_Request) == 'False':
                print "insert kpi failure : {}".format(insert_Request)
                self._pdm.rolleback_transactions()
                return "Failed - Can't delete insert results"

        self._pdm.commit_transactions()
        return "success - data added to the database"

