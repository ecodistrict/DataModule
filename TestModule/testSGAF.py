import DataModule.tcpclient as tcp_client
import json


def main(args=None):
    """
    simulate get Data case
    """

    test_client = tcp_client.TcpClient("10.9.10.183", "Warsaw", "tournaire", "olivier", "5432")
    get_data_message = {
                        "method": "getData",
                        "type": "request",
                        "userId": "cstb",
                        "caseId": "green_factor",
                        "variantId": "asis",
                        "moduleId": "Stockholm_Green_Area_Factor",
                        "calculationId": "3",
                        "eventId": "trout"
                       }
    json_get_data = json.dumps(get_data_message)
    print json_get_data
    test_client.handle_string_event('data', json_get_data)

if __name__ == "__main__":
    main()
