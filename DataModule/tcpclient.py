import imb4
import json
import DataManager
import Stockholm_Green_Area_Factor as SGAF

class TcpClient:
    def __init__(self, localhost, dbname, user, pwd, prt):
        self._connection = imb4.TConnection(imb4.DEFAULT_REMOTE_HOST, imb4.DEFAULT_REMOTE_TLS_PORT, True, 'CSTB', 1)
        self._connection.on_disconnect = self.handle_disconnect

        self._event = self._connection.subscribe('data event',
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


    def write_data(self, data):
        if self._connection.connected:
            print data
            self._event.signal_string_event(data)

    def handle_string_event(self, event_entry, command):
        parsed_json = json.loads(command)
        if parsed_json['method'] == 'createCase':
            retunrDict = {"method" : "createCase", "type" : "response", "userId" : parsed_json["userId"], "caseId" : parsed_json["caseId"]}
            if self._pdm.createSchema(parsed_json['caseId']):
                retunrDict["status"] = "success"
            else:
                retunrDict["status"] = "failed"
            self.write_data(json.dumps(retunrDict))

        elif parsed_json['method'] == 'deleteCase':
            retunrDict = {"method" : "deleteCase", "type" : "response", "userId" : parsed_json["userId"], "caseId" : parsed_json["caseId"]}
            if self._pdm.deleteSchema(parsed_json['caseId']):
                retunrDict["status"] = "success"
            else:
                retunrDict["status"] = "failed"
            self.write_data(json.dumps(retunrDict))

        elif parsed_json['method'] == 'createVariant':
            retunrDict = {"method" : "createVariant", "type" : "response", "userId" : parsed_json["userId"], "caseId" : parsed_json["caseId"], "variantID" : parsed_json["variantID"]}
            schemaID = parsed_json["caseId"] + "_" + parsed_json["variantID"]
            if self._pdm.createSchema(schemaID):
                retunrDict["status"] = "succes"
            else:
                retunrDict["status"] = "failed"
            self.write_data(json.dumps(retunrDict))

        elif parsed_json['method'] == 'deleteVariant':
            retunrDict = {"method" : "deleteVariant", "type" : "response", "userId" : parsed_json["userId"], "caseId" : parsed_json["caseId"], "variantID" : parsed_json["variantID"]}
            schemaID = parsed_json["caseId"] + "_" + parsed_json["variantID"]
            if self._pdm.deleteSchema(schemaID):
                retunrDict["status"] = "succes"
            else:
                retunrDict["status"] = "failed"
            self.write_data(json.dumps(retunrDict))

        elif parsed_json['method'] == 'getData':
            # parse module ID
            returnDict = {"method": "getData", "type": "response", "userId" : parsed_json["userId"],
                          "caseId": parsed_json["caseId"], "variantID" : parsed_json["variantID"],
                          "moduleId": parsed_json["moduleID"]}

            if parsed_json['moduleID'] == 'Stockholm_Green_Area_Factor':
                aModule_SGAF = SGAF.Module_SGAF(self._pdm, parsed_json["caseId"], parsed_json["variantID"])
                returnDict["data"] = aModule_SGAF.getData()
                returnDict["status"] = "succes"
            else:
                returnDict["status"] = "failed"

            self.write_data(json.dumps(returnDict))

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
