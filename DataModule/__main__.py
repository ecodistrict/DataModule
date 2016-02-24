import sys
import tcpclient


def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]

    print("This is the main routine.")
    print("It should do something interesting.")

    # Do argument parsing here (eg. with argparse) and anything else
    # you want your project to do.
    testClient = tcpclient.TcpClient("10.9.10.183", "Hovsjo_test", "tournaire", "olivier", "5432")

    #aTcpclient.write_data("test trout")

    raw_input('waiting on imb commands; press return to quit.. ')


if __name__ == "__main__":
    main()