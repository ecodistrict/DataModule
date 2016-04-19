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

    def executeRequest(self, request):
        if self.isConnected:
            with self.conn.cursor() as cur:
                cur.execute(request)
                return True
        return False

    def commit_transactions(self):
        self.conn.commit()

    def rolleback_transactions(self):
        self.conn.rollback()

    def getDataValue(self, request, cast):
        if self.isConnected:
            with self.conn.cursor() as cur:
                cur.execute(request)
                raw_data = cur.fetchone()
                data = raw_data[0] if type(raw_data) is tuple else raw_data
                if data is not None:
                    if cast is not None:
                        return cast(data)
                    else:
                        return data
        return 0

    def getDataListValues(self, request):
        if self.isConnected:
            with self.conn.cursor() as cur:
                cur.execute(request)
                return cur.fetchall()
        return []

    def getJsonifyValue(self, request):
        if self.isConnected:
            with self.conn.cursor() as cur:
                # add JSON conversion
                json_request = ("""SELECT array_to_json(array_agg(row_to_json(RESULT))) FROM ({}) RESULT""").format(request)
                cur.execute(json_request)
                return cur.fetchone()
        return {}

    def createSchema(self, schemaID):
        if self.checkIfSchemaExists(schemaID):
            return "Success : schema already created before"
        request = ("""SELECT clone_schema('public','{}', TRUE);""").format(schemaID)
        if self.executeRequest(request):
            self.commit_transactions()
            return "Success - schema created"
        else:
            self.rolleback_transactions()
            return "Failed - can't create schema"

    def deleteSchema(self, schemaID):
        if self.checkIfSchemaExists(schemaID):
            return "Success - schema already deleted before"
        request = ("""SELECT drop_schemas('{}');""").format(schemaID)
        if self.executeRequest(request):
            self.commit_transactions()
            return "Success - schema deleted"
        else:
            self.rolleback_transactions()
            return "Failed - can't delete schema"

    def checkIfSchemaExists(self, schemaID):
        request = ("""SELECT schema_name FROM information_schema.schemata WHERE schema_name = '{}';""").format(schemaID);
        if self.isConnected:
            with self.conn.cursor() as cur:
                cur.execute(request)
                raw_data = cur.fetchone()
                data = raw_data[0] if type(raw_data) is tuple else raw_data
                if data is not None:
                    return True
        return False
