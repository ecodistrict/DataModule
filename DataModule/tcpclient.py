import imb4
import json
import DataManager
import Stockholm_Green_Area_Factor as SGAF
import LCC_LCA
import Mobility_Module
import ModuleKPI
import logging


class TcpClient:
    def __init__(self, localhost, db_name, user, pwd, prt):
        self._connection = imb4.TConnection(imb4.DEFAULT_REMOTE_HOST, imb4.DEFAULT_REMOTE_TLS_PORT, True, 'CSTB', 1)
        self._connection.on_disconnect = self.handle_disconnect

        self._data_event = self._connection.subscribe('data',
                                                      on_string_event=self.handle_string_event
                                                      # on_stream_create=self.handle_stream_create,
                                                      # on_stream_end=self.handle_stream_end
                                                      )

        if self._connection.connected:
            print("connected")
        else:
            print("not connected")

        self._pdm = DataManager.PostgresDataManager()
        # testing connection
        self._pdm.connect(localhost, db_name, user, pwd, prt)
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
        type_msg = parsed_json.get('type', 'null')
        if type_msg in ('response', 'null'):
            return

        method = parsed_json.get('method', 'null')
        case_id = parsed_json.get('caseId', 'null')
        user_id = parsed_json.get('userId', 'null')
        variant_id = parsed_json.get('variantId', 'null')

        prefix = 'trout_'
        base_schema_id = case_id if variant_id is None else case_id + "_" + variant_id
        schema_id = prefix + base_schema_id
        db_case_id = prefix + case_id
        calculation_id = parsed_json.get('calculationId', 'null')
        module_id = parsed_json.get('moduleId', 'null')
        event_id = parsed_json.get('eventId', 'data')

        if method == 'createCase':
            return_dict = {"method": method, "type": "response", "userId": user_id, "caseId": case_id}
            if case_id == 'null':
                return_dict["status"] = "failed - no case id"
            if variant_id is not 'null':
                return_dict["status"] = "failed - not supposed to have a variant id"
            elif self._pdm.check_if_schema_exists(db_case_id):
                return_dict["status"] = "Success - schema already created before"
            else:
                return_dict["status"] = "In progress - creating schema"
                self.write_data(json.dumps(return_dict), event_id)
                return_dict["status"] = self._pdm.create_schema(db_case_id)
            self.write_data(json.dumps(return_dict), event_id)

        elif method == 'deleteCase':
            return_dict = {"method": method, "type": "response", "userId": user_id, "caseId": case_id}
            if case_id != 'null':
                return_dict["status"] = "failed - no case id"
            if variant_id is not 'null':
                return_dict["status"] = "failed - not supposed to have a variant id"
            elif not self._pdm.check_if_schema_exists(db_case_id):
                return_dict["status"] = "Success - schema already deleted before"
            else:
                return_dict["status"] = "In progress - deleting cascading schemas"
                self.write_data(json.dumps(return_dict), event_id)
                return_dict["status"] = self._pdm.delete_schema(db_case_id)
            self.write_data(json.dumps(return_dict), event_id)

        elif method == 'createVariant':
            return_dict = {"method": method, "type": "response", "userId": user_id,
                           "caseId": case_id, "variantId": variant_id}
            if case_id == 'null':
                return_dict["status"] = "failed - no case id"
            elif variant_id == 'null':
                return_dict["status"] = "failed - no variant id"
            elif self._pdm.check_if_schema_exists(schema_id):
                return_dict["status"] = "Success - schema already created before"
            elif not self._pdm.check_if_schema_exists(db_case_id):
                return_dict["status"] = "failed - case schema doesn't exist"
            else:
                return_dict["status"] = "In progress - creating schema"
                self.write_data(json.dumps(return_dict), event_id)
                return_dict["status"] = self._pdm.create_schema(schema_id, db_case_id)
            self.write_data(json.dumps(return_dict), event_id)

        elif method == 'deleteVariant':
            return_dict = {"method": method, "type": "response", "userId": user_id,
                           "caseId": case_id, "variantId": variant_id}
            if case_id == 'null':
                return_dict["status"] = "failed - no case id"
            elif variant_id == 'null':
                return_dict["status"] = "failed - no variant id"
            elif not self._pdm.check_if_schema_exists(schema_id):
                return_dict["status"] = "Success - schema already deleted before"
            else:
                return_dict["status"] = "In progress - deleting schema"
                self.write_data(json.dumps(return_dict), event_id)
                return_dict["status"] = self._pdm.delete_schema(schema_id)
            self.write_data(json.dumps(return_dict), event_id)

        elif method == 'getData':
            # parse module ID
            return_dict = {"method": method, "type": "response", "userId": user_id,
                           "caseId": case_id, "variantId": variant_id,
                           "calculationId": calculation_id, "moduleId": module_id}

            if case_id == 'null':
                return_dict["status"] = "failed - no case id"
            elif variant_id == 'null':
                return_dict["status"] = "failed - no variant id"
            elif module_id == 'null':
                return_dict["status"] = "failed - no module id"
            elif not self._pdm.check_if_schema_exists(schema_id):
                return_dict["status"] = "failed - no schema found for case and variant id"
            else:
                if module_id == 'Stockholm_Green_Area_Factor':
                    amodule_sgaf = SGAF.ModuleSGAF(self._pdm, schema_id)
                    return_dict["data"] = amodule_sgaf.get_data()
                    return_dict["status"] = "success"
                elif module_id == 'SP_LCA_v4.0' or module_id == 'SP_LCC_v1.0':
                    amodule_lcc_lca = LCC_LCA.ModuleLCCLCA(self._pdm, schema_id)
                    return_dict["data"] = amodule_lcc_lca.get_data()
                    return_dict["status"] = "success"
                elif module_id == 'MobilityModule':
                    amodule_mobility = Mobility_Module.ModuleMobility(self._pdm, schema_id)
                    return_dict["data"] = amodule_mobility.get_data()
                    return_dict["status"] = "success"
                else:
                    return_dict["status"] = "failed - no module found"
            self.write_data(json.dumps(return_dict), event_id)

        elif method == 'setKpiResult':
            kpi_id = parsed_json.get('kpiId', 'null')
            kpi_value_list = parsed_json.get('kpiValueList', 'null')
            return_dict = {"method": method, "type": "response", "userId": user_id, "caseId": case_id,
                           "variantId": variant_id, "moduleId": module_id, "kpiId": kpi_id}

            if case_id == 'null':
                return_dict["status"] = "failed - no case id"
            elif variant_id == 'null':
                return_dict["status"] = "failed - no variant id"
            elif module_id == 'null':
                return_dict["status"] = "failed - no module id"
            if kpi_id is 'null':
                return_dict["status"] = "failed - no kpiId found in request"
            elif not self._pdm.check_if_schema_exists(schema_id):
                return_dict["status"] = "failed - no schema found for case and variant id"
            else:
                save_module = ModuleKPI.ModuleKPI(self._pdm, schema_id)
                return_dict["status"] = save_module.save(kpi_id, kpi_value_list)
            self.write_data(json.dumps(return_dict), event_id)

        elif method == 'getKpiResult':
            kpi_id = parsed_json.get('kpiId', 'null')
            return_dict = {"method": method, "type": "response", "userId": user_id, "caseId": case_id,
                           "variantId": variant_id, "moduleId": module_id, "kpiId": kpi_id}

            if case_id == 'null':
                return_dict["status"] = "failed - no case id"
            elif variant_id == 'null':
                return_dict["status"] = "failed - no variant id"
            elif module_id == 'null':
                return_dict["status"] = "failed - no module id"
            elif kpi_id is 'null':
                return_dict["status"] = "failed - no kpiId found in request"
            elif not self._pdm.check_if_schema_exists(schema_id):
                return_dict["status"] = "failed - no schema found for case and variant id"
            else:
                load_module = ModuleKPI.ModuleKPI(self._pdm, schema_id)
                return_dict["status"] = load_module.load(kpi_id)
            self.write_data(json.dumps(return_dict), event_id)

        elif method == 'getGeojson':
            return_dict = {"method": method, "type": "response", "userId": user_id, "caseId": case_id,
                           "variantId": variant_id, "moduleId": module_id}

            element_filter = parsed_json.get('element_type_filter', 'null')
            if case_id == 'null':
                return_dict["status"] = "failed - no case id"
            elif variant_id == 'null':
                return_dict["status"] = "failed - no variant id"
            elif module_id == 'null':
                return_dict["status"] = "failed - no module id"
            elif element_filter == 'null':
                return_dict["status"] = "failed - no elements filtered found"
            elif not self._pdm.check_if_schema_exists(schema_id):
                return_dict["status"] = "failed - no schema found for case and variant id"
            else:
                amodule_kpi = ModuleKPI.ModuleKPI(self._pdm, schema_id)
                return_dict['data'] = amodule_kpi.get_geojson(element_filter)
                return_dict["status"] = 'Success - no test on results values'
            self.write_data(json.dumps(return_dict), event_id)

        else:
            logging.warning('## received string event_name: {} command: {}'.format(event_entry.event_name, command))
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

    def handle_disconnect(self):
        logging.info('disconnect')
        print('disconnected..')
