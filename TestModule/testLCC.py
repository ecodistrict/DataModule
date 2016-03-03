import DataModule.tcpclient as tcpclient
import json


def main(args=None):
    """
    simulate get Data case
    """
    getLCCDataMessage = { "method": "getData",
                       "type": "request",
                       "userId": "cstb",
                       "caseId": "truite",
                       "variantId": "test",
                       "moduleId": "LCC",
                       "calculationId" : "3"
                        }
    jsonLCCGetData = json.dumps(getLCCDataMessage)
    print jsonLCCGetData

    getLCADataMessage = { "method": "getData",
                       "type": "request",
                       "userId": "cstb",
                       "caseId": "truite",
                       "variantId": "test",
                       "moduleId": "LCA",
                       "calculationId" : "3"
                        }
    jsonLCAGetData = json.dumps(getLCADataMessage)
    print jsonLCAGetData

    testClient = tcpclient.TcpClient("10.9.10.183", "Hovsjo_test", "tournaire", "olivier", "5432")

    testClient.handle_string_event('data event', getLCADataMessage)
    testClient.handle_string_event('data event', getLCCDataMessage)
    print 'done'


if __name__ == "__main__":
    main()