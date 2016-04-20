import sys
import getopt
import tcpclient
import logging


def main(argv=None):
    """The main routine."""

    logging.basicConfig(filename='dataModule.log', level=logging.DEBUG)

    if argv is None:
        argv = sys.argv[1:]

    host = '10.9.10.183'
    db_name = 'Hovsjo_test'
    user = 'tournaire'
    password = 'olivier'
    port = '5432'
    try:
        opts, args = getopt.getopt(argv, "h:d:u:P:p", ["host=", "dbname=", "user=", "password", "port="])
    except getopt.GetoptError:
        print '__main__.py -h <host> -d <database name> -u <user> -P <password> -p <port>'
        logging.warning('run __main__.py -h <host> -d <database name> -u <user> -P <password> -p <port>')
        logging.warning('or __main__.py --host <host> --dbname <database name> --user <user> --password <password> --port <port>')
        logging.warning('currents args are: {}'.format(args))
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--host'):
            host = arg
        elif opt in ('-d', '--dbname'):
            db_name = arg
        elif opt in ('-u', '--user'):
            user = arg
        elif opt in ('-P', '--password'):
            password = arg
        elif opt in ('-p', '--port'):
            port = arg

    print("Starting dataModule.")
    logging.info("Starting dataModule.")

    # testClient = tcpclient.TcpClient("10.9.10.183", "Hovsjo_test", "tournaire", "olivier", "5432")
    # testClient = tcpclient.TcpClient("localhost", "ecodistrict", "postgres", "FF511Aeris", "5432")
    test_client = tcpclient.TcpClient(host, db_name, user, password, port)
    logging.info('dataModule is running; press return to quit.')
    raw_input('dataModule is running; press return to quit.')

if __name__ == "__main__":
    main()
