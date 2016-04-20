import DataModule.tcpclient as tcpclient
import json


def main(args=None):
    """
    simulate get Data case
    """
    #testClient = tcpclient.TcpClient("10.9.10.183", "Hovsjo_test", "tournaire", "olivier", "5432")
    testClient = tcpclient.TcpClient("localhost", "ecodistrict", "postgres", "FF511Aeris", "5432")

    """
        test get complex kpis message
    """
    getCompexKpisMessage =  {
                                "moduleId": "dashboard",
	                            "variantId": "greenfactoralt1",
	                            "caseId": "hovsjo",
	                            "userId": "cstb",
                                "method": "getKpiResult",
                                "kpiId": "change-of-primary-energy-use-per-heated-area",
                                "type": "request",
                                "eventId": "trout"
                            }

    jsonGetComplexKpis = json.dumps(getCompexKpisMessage)
    print jsonGetComplexKpis
    testClient.handle_string_event('data', jsonGetComplexKpis)


    """
        test get geoJSON response message
    """
    getGeoJSONDataMessage = {
	                            "variantId": "lcalccalt4b",
	                            "caseId": "hovsjo",
	                            "userId": "cstb",
                                "method": "get_geojson",
                                "type": "request",
                                "eventId": "trout",
                                "element_type_filter": "building"
                            }

    jsonGetGeoJSONData = json.dumps(getGeoJSONDataMessage)
    print jsonGetGeoJSONData

    testClient.handle_string_event('data', jsonGetGeoJSONData)

if __name__ == "__main__":
	main()
