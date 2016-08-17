import DataModule.UploadData as UploadData
from Tkinter import Tk
from tkFileDialog import askopenfilename

def main(args=None):
    uploader = UploadData.UploadFromGeoJSON()

    Tk().withdraw()
    filename = askopenfilename()

    uploader.schemaID = 'trout_test_temp'
    uploader.upload_data(filename)


if __name__ == "__main__":
    main()
