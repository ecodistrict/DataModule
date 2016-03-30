import psycopg2


class PostresDataManager:
    def __init__(self):
        self.isConnected = False

    def __del__(self):
        if self.isConnected:
            self.conn.close()

    def connect(self, host, dbname, user, password,port):
        self.isConnected = False
        try:
             self.conn = psycopg2.connect(dbname=dbname, user=user, host=host, password=password, port=port)
             self.isConnected = True
        except:
             print "I am unable to connect to the database"

    def isConnect(self):
        return self.isConnected

    def _executeRequest(self, request):
        ret = False
        if self.isConnected:
            cur = self.conn.cursor()
            try:
                cur.execute(request)
                self.conn.commit()
                ret = True
            except:
                ret = False
            cur.close()
        return ret

    def getDataValue(self, request, cast):
        ret = 0
        if self.isConnected:
            cur = self.conn.cursor()
            try:
                cur.execute(request)
                data = cur.fetchone()
                if data[0] is not None:
                    ret = cast(data[0])
            except:
                pass
            cur.close()
        return ret

    def getJsonifyValue(self, request):
        if self.isConnected:
            cur = self.conn.cursor()
            try:
                # add JSON conversion
                json_request = ("""SELECT array_to_json(array_agg(row_to_json(RESULT))) FROM ({}) RESULT""").format(request)
                cur.execute(json_request)
                data = cur.fetchone()
            except:
                data = {}
                pass
            cur.close()
        return data

    def createSchema(self, schemaID):
        if self.checkIfSchemaExists(schemaID):
            return "Success : schema already created before"
        request = ("""SELECT clone_schema('public','{}', TRUE);""").format(schemaID)
        if self._executeRequest(request):
            return "Success - schema created"
        else:
            return "Failed - can't create schema"

    def deleteSchema(self, schemaID):
        if self.checkIfSchemaExists(schemaID):
            return "Success - schema already deleted before"
        request = ("""SELECT drop_schemas('{}');""").format(schemaID)
        if self._executeRequest(request):
            return "Success - schema deleted"
        else:
            return "Failed - can't delete schema"

    def checkIfSchemaExists(self, schemaID):
        request = ("""SELECT schema_name FROM information_schema.schemata WHERE schema_name = '{}';""").format(schemaID);
        ret = False
        if self.isConnected:
            cur = self.conn.cursor()
            try:
                cur.execute(request)
                data = cur.fetchone()
                if data[0] is not None:
                    ret = True
            except:
                pass
            cur.close()
        return ret