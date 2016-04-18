import sys
import tcpclient

def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]

    print("Starting dataModule.")

    #testClient = tcpclient.TcpClient("10.9.10.183", "Hovsjo_test", "tournaire", "olivier", "5432")
    testClient = tcpclient.TcpClient("localhost", "ecodistrict", "postgres", "FF511Aeris", "5432")
    raw_input('dataModule is running; press return to quit.')

if __name__ == "__main__":
    main()