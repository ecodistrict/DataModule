import DataModule.DataManager as DataManager


def main(args=None):
    pdm = DataManager.PostgresDataManager()
    pdm.connect("10.9.10.183", "Hovsjo_test", "tournaire", "olivier", "5432")
    pdm.createSchema('trout')

    print 'done'


if __name__ == "__main__":
    main()