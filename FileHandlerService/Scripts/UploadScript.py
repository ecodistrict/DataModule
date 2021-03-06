import UploadModule.UploadData as UploadData

import sys
import getopt
import logging


class UploadScript:
    def __init__(self, file, extension, case_id, variant_id):
        print("UploadScript")
        print("   extension: %s" % extension)
        print("   case_id: %s" % case_id)
        print("   variant_id: %s" % variant_id)
        
        logging.basicConfig(filename='UploadModule.log', level=logging.DEBUG)
        logging.FileHandler('UploadModule.log', mode='w')

        try:
            logging.info("currents args are: {}".format(sys.argv[1:]))
            opts, args = getopt.getopt(sys.argv[1:], "h:d:u:P:p:f:", ["host=", "dbname=", "user=", "password", "port=", "filename="])
        except getopt.GetoptError:
            logging.warning('run UploadScript.py -h <host> -d <database name> -u <user> -P <password> -p <port> -f <filename> ')
            logging.warning('or UploadScript.py --host <host> --dbname <database name> --user <user> --password <password> --port <port> --filename <filename>')
            sys.exit(2)
        for opt, arg in opts:
            if opt in ('-h', '--host'):
                host = arg
            elif opt in ('-d', '--dbname'):
                db_name = arg
            elif opt in ('-u', '--user'):
                user = arg
            elif opt in ('-P', '--password'):
                password = arg
            elif opt in ('-p', '--port'):
                port = arg
            elif opt in ('-f', '--filename'):
                filename = arg

        logging.info("Starting UploadModule.")

        uploader = UploadData.UploadModule(host, db_name, user, password, port, case_id, variant_id)
        print("created UploadModule")
        self._status = uploader.upload_data(file, extension)
        print("after uploader.upload_data")
        logging.info('finished')

    def getStatus(self):
        return self._status
