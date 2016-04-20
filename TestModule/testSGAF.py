import DataModule.tcpclient as tcpclient
import json


def main(args=None):
    """
    simulate get Data case
    """
    getDataMessage = { "method": "get_data",
                       "type": "request",
                       "userId": "cstb",
                       "caseId": "hovsjo",
                       "variantId": "greenfactoralt2",
                       "moduleId": "Stockholm_Green_Area_Factor",
                       "calculationId" : "3",
                       "eventId" : "trout"
                        }
    jsonGetData = json.dumps(getDataMessage)
    print jsonGetData

    testClient = tcpclient.TcpClient("10.9.10.183", "Hovsjo_test", "tournaire", "olivier", "5432")
    testClient.handle_string_event('data', jsonGetData)

    # pdm = DataManager.PostresDataManager()
    # pdm.connect("10.9.10.183", "Hovsjo_test", "tournaire", "olivier", "5432")
    # pdm.create_schema('truite_test')
    # sgafTest = SGAF.Module_SGAF(pdm, "truite", "test")
    # sgafTest.get_data()

    print 'done'


if __name__ == "__main__":
    main()