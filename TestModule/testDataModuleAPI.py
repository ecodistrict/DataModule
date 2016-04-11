import DataModule.tcpclient as tcpclient
import json



def main(args=None):
    """
    """

    """
    Create case
    """
    createCaseMessage = { "method": "createCase",
                          "type": "request",
                          "userId": "cstb",
                          "caseId": "stockholm"
                        }
    jsoncreateCase = json.dumps(createCaseMessage)
    print jsoncreateCase

    testClient = tcpclient.TcpClient("10.9.10.183", "Hovsjo_test", "tournaire", "olivier", "5432")
    testClient.handle_string_event('data', jsoncreateCase)


    """
    Create 2 Variants
    """
    createVariant1Message = { "method": "createVariant",
                             "type": "request",
                             "userId": "cstb",
                             "caseId": "stockholm",
                             "variantId" : "asis"
                            }
    jsoncreateVariant1 = json.dumps(createVariant1Message)
    print jsoncreateVariant1

    testClient.handle_string_event('data', jsoncreateVariant1)

    createVariant2Message = { "method": "createVariant",
                             "type": "request",
                             "userId": "cstb",
                             "caseId": "stockholm",
                             "variantId" : "renoved"
                            }
    jsoncreateVariant2 = json.dumps(createVariant2Message)
    print jsoncreateVariant2

    testClient.handle_string_event('data', jsoncreateVariant2)

    """
    Delete one variant
    """
    deleteVariant1Message = { "method": "deleteVariant",
                             "type": "request",
                             "userId": "cstb",
                             "caseId": "stockholm",
                             "variantId" : "renoved"
                            }
    jsondeleteVariant = json.dumps(deleteVariant1Message)
    print jsondeleteVariant

    testClient.handle_string_event('data', jsondeleteVariant)


    """
    Delete case and last associated variant
    """
    deleteCaseMessage = { "method": "deleteCase",
                          "type": "request",
                          "userId": "cstb",
                          "caseId": "stockholm"
                        }
    jsondeleteCase = json.dumps(deleteCaseMessage)

    print jsondeleteCase

    testClient.handle_string_event('data', jsondeleteCase)


if __name__ == "__main__":
    main()