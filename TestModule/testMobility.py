import DataModule.tcpclient as tcp_client
import json


def main(args=None):
    """
    simulate get Data case
    """
    test_client = tcp_client.TcpClient("10.9.10.183", "Warsaw", "tournaire", "olivier", "5432")
    # test_client = tcp_client.TcpClient("localhost", "ecodistrict", "postgres", "FF511Aeris", "5432")

    get_data_message_mobility = {
                                "method": "getData",
                                "type": "request",
                                "userId": "cstb",
                                "caseId": "hovsjo",
                                "variantId": "mobilityalt1",
                                "moduleId": "MobilityModule",
                                "calculationId": "xx_mobility_xx",
                                'eventId': "trout"
                                }
    json_get_data_mobility = json.dumps(get_data_message_mobility)
    print json_get_data_mobility
    test_client.handle_string_event('data', json_get_data_mobility)

if __name__ == "__main__":
    main()
