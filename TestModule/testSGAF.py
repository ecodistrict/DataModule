import DataModule.Stockholm_Green_Area_Factor as SGAF
import DataModule.tcpclient as tcpclient
import json


def main(args=None):
    """
    simulate get Data case
    """
    getDataMessage = { "method": "getData",
                       "type": "request",
                       "userId": "cstb",
                       "caseId": "truite",
                       "variantId": "test",
                       "moduleId": "Stockholm_Green_Area_Factor",
                       "calculationId" : "3"
                        }
    jsonGetData = json.dumps(getDataMessage)
    print jsonGetData

    testClient = tcpclient.TcpClient("10.9.10.183", "Hovsjo_test", "tournaire", "olivier", "5432")
    testClient.handle_string_event('data event', jsonGetData)

    # pdm = DataManager.PostresDataManager()
    # pdm.connect("10.9.10.183", "Hovsjo_test", "tournaire", "olivier", "5432")
    # pdm.createSchema('truite_test')
    # sgafTest = SGAF.Module_SGAF(pdm, "truite", "test")
    # sgafTest.getData()

    print 'done'


if __name__ == "__main__":
    main()