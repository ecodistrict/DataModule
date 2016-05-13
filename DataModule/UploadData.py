import json
import Abstract_Module

class UploadFromGeoJSON(Abstract_Module.AbstractModule):
    def __init__(self):
        self._json_dict = {}

    def upload_local_file(self, fileURL):
        with open(fileURL) as json_file:
            self._json_dict = json.load(json_file)

    def printJSON(self):
        print self._json_dict
