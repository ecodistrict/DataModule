import DataModule.tcpclient as tcpclient
import json


def main(args=None):
    """
    simulate get Data case
    """
    #testClient = tcpclient.TcpClient("10.9.10.183", "Hovsjo_test", "tournaire", "olivier", "5432")
    testClient = tcpclient.TcpClient("localhost", "ecodistrict", "postgres", "FF511Aeris", "5432")

    getDataMessageMobility = {"method": "get_data",
                       "type": "request",
                       "userId": "cstb",
                       "caseId": "hovsjo",
                       "variantId": "mobilityalt1",
                       "moduleId": "MobilityModule",
                       "calculationId" : "xx_mobility_xx"
                        }
    jsonGetDataMobility = json.dumps(getDataMessageMobility)
    print jsonGetDataMobility

    testClient.handle_string_event('data', jsonGetDataMobility)


if __name__ == "__main__":
    main()