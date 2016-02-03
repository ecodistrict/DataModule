import psycopg2


class PostresDataManager:
    def __init__(self):
        self.isConnected = False

    def __del__(self):
        if self.isConnected:
            self.conn.close()

    def connect(self, host, dbname, user, password):
        self.isConnected = False
        try:
             self.conn = psycopg2.connect(dbname=dbname, user=user, host=host, password=password)
             self.isConnected = True
        except:
             print "I am unable to connect to the database"

    def isConnect(self):
        return self.isConnected

    def _executeRequest(self, request):
        ret = False;
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

    def createSchema(self, schemaID):
        request = ("""SELECT clone_schema('public','{}');""").format(schemaID)
        return self._executeRequest(request)

    def deleteSchema(self, schemaID):
        request = ("""SELECT drop_schemas('{}');""").format(schemaID)
        return self._executeRequest(request)