import DataModule.tcpclient as tcpclient
import json


def main(args=None):
    """
    simulate get Data case
    """
    testClient = tcpclient.TcpClient("10.9.10.183", "Hovsjo_test", "tournaire", "olivier", "5432")

    getDataMessageLCC = {"method": "getData",
                       "type": "request",
                       "userId": "cstb",
                       "caseId": "hovsjo",
                       "variantId": "greenfactoralt1",
                       "moduleId": "SP_LCC_v1.0",
                       "calculationId" : "4"
                        }
    jsonGetDataLCC = json.dumps(getDataMessageLCC)
    print jsonGetDataLCC

    testClient.handle_string_event('data event', jsonGetDataLCC)


    getDataMessageLCA = {"method": "getData",
                       "type": "request",
                       "userId": "cstb",
                       "caseId": "hovsjo",
                       "variantId": "greenfactoralt1",
                       "moduleId": "SP_LCA_v4.0",
                       "calculationId" : "5"
                        }
    jsonGetDataLCA = json.dumps(getDataMessageLCA)
    print jsonGetDataLCA

    testClient.handle_string_event('data event', jsonGetDataLCA)


if __name__ == "__main__":
    main()