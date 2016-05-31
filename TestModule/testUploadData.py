import DataModule.UploadData as UploadData

def main(args=None):
    uploader = UploadData.UploadFromGeoJSON()
    uploader.upload_local_file("./data/Warsaw.geojson")
    uploader.print_json()

    uploader.upload_buildings_geometry()

if __name__ == "__main__":
    main()
