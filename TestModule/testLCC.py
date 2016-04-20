import DataModule.tcpclient as tcpclient
import json


def main(args=None):
    """
    simulate get Data case
    """
    testClient = tcpclient.TcpClient("10.9.10.183", "Hovsjo_test", "tournaire", "olivier", "5432")

    getDataMessageLCC = {"method": "get_data",
                       "type": "request",
                       "userId": "cstb",
                       "caseId": "hovsjo",
                       "variantId": "lcalccalt4b",
                       "moduleId": "SP_LCC_v1.0",
                       "calculationId" : "4"
                        }
    jsonGetDataLCC = json.dumps(getDataMessageLCC)
    print jsonGetDataLCC

    testClient.handle_string_event('data', jsonGetDataLCC)


    getDataMessageLCA = {"method": "get_data",
                       "type": "request",
                       "userId": "cstb",
                       "caseId": "hovsjo",
                       "variantId": "lcalccalt4b",
                       "moduleId": "SP_LCA_v4.0",
                       "calculationId" : "5",
                       "eventId" : "data"
                        }
    jsonGetDataLCA = json.dumps(getDataMessageLCA)
    print jsonGetDataLCA

    testClient.handle_string_event('data', jsonGetDataLCA)


if __name__ == "__main__":
    main()