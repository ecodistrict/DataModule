import DataModule.tcpclient as tcp_client
import json


def main(args=None):
    """
    """

    """
    Create case
    """
    create_case_message = {
                            "method": "createCase",
                            "type": "request",
                            "userId": "cstb",
                            "caseId": "stockholm"
                          }
    jsoncreateCase = json.dumps(create_case_message)
    print jsoncreateCase

    test_client = tcp_client.TcpClient("10.9.10.183", "Warsaw", "tournaire", "olivier", "5432")
    # test_client = tcp_client.TcpClient("localhost", "ecodistrict", "postgres", "FF511Aeris", "5432")
    test_client.handle_string_event('data', jsoncreateCase)

    """
    Create 2 Variants
    """
    create_variant1_message = {
                                "method": "createVariant",
                                "type": "request",
                                "userId": "cstb",
                                "caseId": "stockholm",
                                "variantId": "asis",
                                "eventId": "trout"
                              }
    json_create_variant1 = json.dumps(create_variant1_message)
    print json_create_variant1
    test_client.handle_string_event('data', json_create_variant1)

    create_variant2_message = {
                                "method": "createVariant",
                                "type": "request",
                                "userId": "cstb",
                                "caseId": "stockholm",
                                "variantId": "renoved",
                                "eventId": "trout"
                              }
    json_create_variant2 = json.dumps(create_variant2_message)
    print json_create_variant2
    test_client.handle_string_event('data', json_create_variant2)

    """
    Delete one variant
    """
    delete_variant1_message = {
                                "method": "deleteVariant",
                                "type": "request",
                                "userId": "cstb",
                                "caseId": "stockholm",
                                "variantId": "renoved",
                                "eventId": "trout"
                              }
    json_delete_variant = json.dumps(delete_variant1_message)
    print json_delete_variant
    test_client.handle_string_event('data', json_delete_variant)

    """
    Delete case and last associated variant
    """
    delete_case_message = {
                            "method": "deleteCase",
                            "type": "request",
                            "userId": "cstb",
                            "caseId": "stockholm",
                            "eventId": "trout"
                          }
    json_delete_case = json.dumps(delete_case_message)
    print json_delete_case
    test_client.handle_string_event('data', json_delete_case)

if __name__ == "__main__":
    main()
