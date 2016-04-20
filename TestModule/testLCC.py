import DataModule.tcpclient as tcp_client
import json


def main(args=None):
    """
    """

    """
    simulate get Data LCC case
    """
    test_client = tcp_client.TcpClient("10.9.10.183", "Hovsjo_test", "tournaire", "olivier", "5432")

    get_data_message_lcc = {
                            "method": "get_data",
                            "type": "request",
                            "userId": "cstb",
                            "caseId": "hovsjo",
                            "variantId": "lcalccalt4b",
                            "moduleId": "SP_LCC_v1.0",
                            "calculationId": "4",
                            "eventId": "trout"
                           }
    json_get_data_lcc = json.dumps(get_data_message_lcc)
    print json_get_data_lcc
    test_client.handle_string_event('data', json_get_data_lcc)

    """
    simulate get Data LCA case
    """
    get_data_message_lca = {
                            "method": "getData",
                            "type": "request",
                            "userId": "cstb",
                            "caseId": "hovsjo",
                            "variantId": "lcalccalt4b",
                            "moduleId": "SP_LCA_v4.0",
                            "calculationId": "5",
                            "eventId": "trout"
                           }
    json_get_data_lca = json.dumps(get_data_message_lca)
    print json_get_data_lca
    test_client.handle_string_event('data', json_get_data_lca)

if __name__ == "__main__":
    main()
