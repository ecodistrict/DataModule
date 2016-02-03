import DataModule.DataManager as DataManager


def main(args=None):
    pdm = DataManager.PostresDataManager()
    pdm.connect("localhost", "ecodistrict", "flachet", "truitos")
    pdm.createSchema('trout')

    print 'done'


if __name__ == "__main__":
    main()