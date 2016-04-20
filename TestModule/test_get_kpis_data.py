import DataModule.tcpclient as tcp_client
import json


def main(args=None):
    """
    simulate get Data case
    """
    #test_client = tcp_client.TcpClient("10.9.10.183", "Hovsjo_test", "tournaire", "olivier", "5432")
    test_client = tcp_client.TcpClient("localhost", "ecodistrict", "postgres", "FF511Aeris", "5432")

    """
        test get complex kpis message
    """
    get_complex_kpi_message = {
                                "moduleId": "dashboard",
                                "variantId": "greenfactoralt1",
                                "caseId": "hovsjo",
                                "userId": "cstb",
                                "method": "getKpiResult",
                                "kpiId": "change-of-primary-energy-use-per-heated-area",
                                "type": "request",
                                "eventId": "trout"
                              }

    json_get_complex_kpi = json.dumps(get_complex_kpi_message)
    print json_get_complex_kpi
    test_client.handle_string_event('data', json_get_complex_kpi)

    """
        test get geoJSON response message
    """
    get_geojson_data_message = {
                                "variantId": "lcalccalt4b",
                                "caseId": "hovsjo",
                                "userId": "cstb",
                                "method": "get_geojson",
                                "type": "request",
                                "eventId": "trout",
                                "element_type_filter": "building"
                               }

    json_get_geojson_data = json.dumps(get_geojson_data_message)
    print json_get_geojson_data
    test_client.handle_string_event('data', json_get_geojson_data)

if __name__ == "__main__":
    main()
