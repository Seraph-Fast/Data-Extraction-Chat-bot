#data_pipeline code
from llama_index.core import SimpleDirectoryReader
def get_data():

    # def download_files_from_google_drive(credentials_file, folder_id):
    #     gauth = GoogleAuth()
    #     gauth.LoadClientConfigFile(credentials_file)
    #     gauth.LocalWebserverAuth()
    #     drive = GoogleDrive(gauth)
    #     query = f"'{folder_id}' in parents and trashed=false"
    #     file_list = drive.ListFile({'q': query}).GetList()
        
    #     for file in file_list:
    #         print(f'Downloading {file["title"]} from Google Drive...')
    #         temp_file_path = os.path.join(temp_dir, file['title'])
    #         file_io = io.FileIO(temp_file_path, 'wb')
    #         request = drive.auth.service.files().get_media(fileId=file['id'])
    #         downloader = MediaIoBaseDownload(file_io, request)
    #         done = False
    #         while not done:
    #             _, done = downloader.next_chunk()
    #         file_io.close()

    #     print("Completed downloading all files from Google Drive.")

    # def download_files_from_s3(region, access_key, secret_access_key, bucket_name):
    #     s3 = boto3.resource(
    #         's3',
    #         aws_access_key_id=access_key,
    #         aws_secret_access_key=secret_access_key,
    #         region_name=region
    #     )
    #     bucket = s3.Bucket(bucket_name)
    #     for obj in bucket.objects.all():
    #         file_path = os.path.join(temp_dir, obj.key)
    #         bucket.download_file(obj.key, file_path)
    #         print(f"Downloaded {obj.key} from AWS S3 to {file_path}")

    # def download_files_from_dropbox(access_token, path=""):
    #     try:
    #         dbx = dropbox.Dropbox(access_token)
    #         files = dbx.files_list_folder(path).entries
    #         for file_metadata in files:
    #             if isinstance(file_metadata, dropbox.files.FileMetadata):
    #                 file_path = file_metadata.path_lower
    #                 temp_file_path = os.path.join(temp_dir, os.path.basename(file_path))
    #                 _, result = dbx.files_download(file_path)
    #                 with open(temp_file_path, 'wb') as f:
    #                     f.write(result.content)
    #                 print(f"Downloaded {file_path} from Dropbox to {temp_file_path}")
    #     except AuthError as e:
    #         print('Error downloading from Dropbox: ' + str(e))
    #     except ApiError as e:
    #         print('API error: ' + str(e))

    # # Google Drive
    # google_credential_file = '-'
    # google_folder_id = '-'

    # # Dropbox
    # dropbox_access_token = "-"

    # # AWS S3
    # aws_region = "-"
    # aws_access_key_id = "-"
    # aws_secret_access_key = "-"
    # aws_bucket_name = '-'

    # with tempfile.TemporaryDirectory() as temp_dir:
        
    #     #download_files_from_google_drive(google_credential_file, google_folder_id)    

    #     download_files_from_dropbox(dropbox_access_token)    

    #     #download_files_from_s3(aws_region, aws_access_key_id, aws_secret_access_key, aws_bucket_name)

    #     documents = SimpleDirectoryReader(temp_dir, filename_as_id=True).load_data()    

    #     print(f"All files are temporarily stored in {temp_dir}")

    documents = SimpleDirectoryReader('file_directory', filename_as_id=True).load_data()
    return documents
