import imb4
import json
import DataManager
import Stockholm_Green_Area_Factor as SGAF
import LCC_LCA
import ModuleKPI

class TcpClient:
    def __init__(self, localhost, dbname, user, pwd, prt):
        self._connection = imb4.TConnection(imb4.DEFAULT_REMOTE_HOST, imb4.DEFAULT_REMOTE_TLS_PORT, True, 'CSTB', 1)
        self._connection.on_disconnect = self.handle_disconnect

        self._data_event = self._connection.subscribe('data',
                                                      on_string_event=self.handle_string_event
                                                      #on_stream_create=self.handle_stream_create,
                                                      #on_stream_end=self.handle_stream_end
                                                      )

        if self._connection.connected:
            print("connected")
        else:
            print("not connected")

        self._pdm = DataManager.PostresDataManager()
        # testing connection
        self._pdm.connect(localhost, dbname, user, pwd, prt)
        if self._pdm.isConnected:
            print "Postgres is connected"
        else:
            print "error in Postgres connection"


    def write_data(self, data, event_name):
        if self._connection.connected:
            print data
            event = self._connection.publish(event_name)
            event.signal_string_event(data)

    def handle_string_event(self, event_entry, command):
        parsed_json = json.loads(command)
        method = parsed_json.get('method', 'null')
        case_id = parsed_json.get('caseId', 'null')
        user_id = parsed_json.get('userId', 'null')
        variant_id = parsed_json.get('variantId', None)
        schema_id = case_id if variant_id is None else case_id + "_" + variant_id
        calculation_id = parsed_json.get('calculationId', 'null')
        module_id = parsed_json.get('moduleId', 'null')
        event_id = parsed_json.get('eventId', 'data')

        if method == 'createCase':
            returnDict = {"method" : method, "type" : "response", "userId" : user_id, "caseId" : case_id}
            if case_id == 'null':
                returnDict["status"] = "failed - no case id"
            else:
                returnDict["status"] = self._pdm.createSchema(case_id)
            self.write_data(json.dumps(returnDict), event_id)

        elif method == 'deleteCase':
            returnDict = {"method" : method, "type" : "response", "userId" : user_id, "caseId" : case_id}
            if case_id != 'null':
                returnDict["status"] = "failed - no case id"
            else:
                returnDict["status"] = self._pdm.deleteSchema(case_id)
            self.write_data(json.dumps(returnDict), event_id)

        elif method == 'createVariant':
            returnDict = {"method" : method, "type" : "response", "userId" : user_id, "caseId" : case_id, "variantId" : variant_id}
            if case_id == 'null':
                returnDict["status"] = "failed - no case id"
            elif variant_id == 'null':
                returnDict["status"] = "failed - no variant id"
            else:
                returnDict["status"] = self._pdm.createSchema(schema_id, case_id)
            self.write_data(json.dumps(returnDict), event_id)

        elif method == 'deleteVariant':
            returnDict = {"method" : method, "type" : "response", "userId" : user_id, "caseId" : case_id, "variantId" : variant_id}
            if case_id == 'null':
                returnDict["status"] = "failed - no case id"
            elif variant_id == 'null':
                returnDict["status"] = "failed - no variant id"
            else:
                returnDict["status"] = self._pdm.deleteSchema(schema_id)
            self.write_data(json.dumps(returnDict), event_id)

        elif method == 'getData':
            # parse module ID
            returnDict = {"method": method, "type": "response", "userId" : user_id,
                          "caseId": case_id, "variantId" : variant_id,
                          "calculationId" : calculation_id, "moduleId": module_id}

            if case_id == 'null':
                returnDict["status"] = "failed - no case id"
            elif variant_id == 'null':
                returnDict["status"] = "failed - no variant id"
            elif module_id == 'null':
                returnDict["status"] = "failed - no module id"
            else:
                if module_id == 'Stockholm_Green_Area_Factor':
                    aModule_SGAF = SGAF.Module_SGAF(self._pdm, schema_id)
                    returnDict["data"] = aModule_SGAF.getData()
                    returnDict["status"] = "succes"
                elif module_id == 'SP_LCA_v4.0' or module_id == 'SP_LCC_v1.0':
                    aModule_LCC_LCAA = LCC_LCA.Module_LCC_LCA(self._pdm, schema_id)
                    returnDict["data"] = aModule_LCC_LCAA.getData()
                    returnDict["status"] = "succes"
                else:
                    returnDict["status"] = "failed - no module found"
            self.write_data(json.dumps(returnDict), event_id)

        elif method == 'setKpiResult':
            kpi_id = parsed_json.get('kpiId', 'null')
            kpiValueList = parsed_json.get('kpiValueList', 'null')
            returnDict = {"method": method, "type": "response", "userId": user_id, "caseId": case_id,
                          "variantId": variant_id, "moduleId": module_id, "kpiId": kpi_id}

            saveModule = ModuleKPI.Module_KPI(self._pdm, schema_id)
            returnDict["status"] = saveModule.save(kpi_id, kpiValueList)
            self.write_data(json.dumps(returnDict), event_id)

        elif method == 'getKpiResult':
            kpi_id = parsed_json.get('kpiId', 'null')
            returnDict = {"method": method, "type": "response", "userId": user_id, "caseId": case_id,
                      "variantId": variant_id, "moduleId": module_id, "kpiId": kpi_id}

            loadModule = ModuleKPI.Module_KPI(self._pdm, schema_id)
            returnDict["status"] = loadModule.load(kpi_id)
            self.write_data(json.dumps(returnDict), event_id)

        elif method == 'getGeoJson':
            returnDict = {"method": method, "type": "response", "userId": user_id, "caseId": case_id,
                          "variantId": variant_id, "moduleId": module_id}

            element_filter = parsed_json.get('element_type_filter', 'null')
            if element_filter == 'null':
                returnDict["status"] = "failed - no elements filtered found"
            else:
                aKpiModule = ModuleKPI.Module_KPI(self._pdm, schema_id)
                returnDict['data'] = aKpiModule.getGeoJson(element_filter)
                returnDict["status"] = 'Success - no test on results values'
            self.write_data(json.dumps(returnDict), event_id)

        else:
            print('## received string', event_entry.event_name, command)

    # def handle_stream_create(self, event_entry, stream_name):
    #     if stream_name == 'a stream name':
    #         print('OK received stream create', event_entry.event_name, stream_name)
    #     else:
    #         print('## received stream create', event_entry.event_name, stream_name)
    #
    # def handle_stream_end(self, event_entry, stream, stream_name, cancel):
    #     if stream and stream_name == 'a stream name' and not cancel:
    #         print('OK received stream end', event_entry.event_name, stream_name, cancel)
    #     else:
    #         print('## received stream end', event_entry.event_name, stream_name, cancel)

    def handle_disconnect(_):
        print('disconnected..')
