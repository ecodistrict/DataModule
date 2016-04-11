import DataModule.tcpclient as tcpclient
import json


def main(args=None):
    """
    simulate get Data case
    """
    testClient = tcpclient.TcpClient("10.9.10.183", "Hovsjo_test", "tournaire", "olivier", "5432")

    getGeoJSONDataMessage = {
	                    "variantId": "lcalccalt4b",
	                    "caseId": "hovsjo",
	                    "userId": "cstb",
                        "method": "getGeoJson",
                        "type": "request"
                    }

    jsonGetGeoJSONData = json.dumps(getGeoJSONDataMessage)
    print jsonGetGeoJSONData

    testClient.handle_string_event('data', jsonGetGeoJSONData)

if __name__ == "__main__":
	main()
