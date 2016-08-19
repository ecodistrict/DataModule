import DataModule.UploadData as UploadData
from Tkinter import Tk
from tkFileDialog import askopenfilename

def main(args=None):
    uploader = UploadData.UploadModule()
    Tk().withdraw()
    filename = askopenfilename()
    uploader.upload_data(filename)
    print 'finished'

if __name__ == "__main__":
    main()
