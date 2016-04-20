import DataModule.tcpclient as tcp_client
import json


def main(args=None):
    """
    simulate get Data case
    """
    test_client = tcp_client.TcpClient("10.9.10.183", "Hovsjo_test", "tournaire", "olivier", "5432")

    save_data_message = {
        "moduleId": "SP_LCA_v4.0",
        "variantId": "greenfactoralt1",
        "caseId": "hovsjo",
        "userId": "cstb",
        "eventId": "trout",
        "kpiId": "change-of-primary-energy-use-per-heated-area",
        "kpiValueList": [{
            "type": "building",
            "gml_id": "NAME_ID_000",
            "kpiId": "change-of-primary-energy-use-per-heated-area",
            "kpiValue": -8155771.9535738109
        },
            {
                "type": "building",
                "gml_id": "NAME_ID_001",
                "kpiId": "change-of-primary-energy-use-per-heated-area",
                "kpiValue": -9294355.020351842
            }],
        "method": "setKpiResult",
        "type": "request"
    }

    json_save_data = json.dumps(save_data_message)
    print json_save_data
    test_client.handle_string_event('data', json_save_data)


if __name__ == "__main__":
    main()
