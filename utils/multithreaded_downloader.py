from google.cloud import storage
from google.cloud.storage import Blob
import os
import os.path
from threading import Thread

def download_blob(bucket_name, key_path, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    # The ID of your GCS bucket
    #bucket_name = "dev-nd-screenomics"

    # The ID of your GCS object
    # source_blob_name = "storage-object-name"

    # The path to which the file should be downloaded
    # destination_file_name = "local/path/to/file"

    #storage_client = storage.Client()
    storage_client = storage.Client.from_service_account_json(json_credentials_path=key_path)

    bucket = storage_client.bucket(bucket_name)

    # Construct a client side representation of a blob.
    # Note `Bucket.blob` differs from `Bucket.get_blob` as it doesn't retrieve
    # any content from Google Cloud Storage. As we don't need additional data,
    # using `Bucket.blob` is preferred here.
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)

    print(
        "Downloaded storage object {} from bucket {} to local file {}.".format(
            source_blob_name, bucket_name, destination_file_name
        )
    )

def download_thread(prefix: str):
    data_folder = "/home/mcurran2/gcloud"
    key_path = "/home/mcurran2/gcloud/bucket_key.json"
    client = storage.Client.from_service_account_json(json_credentials_path=key_path)
    #src_bucket = client.get_bucket(SRC_BUCKET_NAME)
    #dst_bucket = client.get_bucket(DST_BUCKET_NAME)
    #key_bucket = client.get_bucket(KEY_BUCKET_NAME)

    #keys = client.list_blobs(KEY_BUCKET_NAME)

    #for keyfile in keys:
    #    print(keyfile.name)
    #    if keyfile.name == "87ea235a":
    #        blobs = client.list_blobs(SRC_BUCKET_NAME, prefix=keyfile.name + "/2023_01")
    #        for blob in blobs:
    #            print(blob.name)

    DEV_BUCKET = "dev-nd-screenomics"
    SRC_BUCKET_NAME = "final-screenomics"
    #dev_bucket = client.get_bucket(DEV_BUCKET)
    keys = client.list_blobs(SRC_BUCKET_NAME, prefix=prefix, max_results=5)
    #srcbucket = storage.Bucket(client, DEV_BUCKET)
    #dstbucket = storage.Bucket(client, DST_BUCKET_NAME)
    for blob in keys:
        print(blob.name)
        name_parts = blob.name.split('/')
        if len(name_parts) == 2 and name_parts[1][-3:] == 'png':
            if not os.path.isdir(os.path.join(data_folder, name_parts[0])):
                os.mkdir(os.path.join(data_folder, name_parts[0]))
            download_blob(SRC_BUCKET_NAME, key_path, blob.name, os.path.join(data_folder, blob.name))
            if os.path.exists(os.path.join(data_folder, blob.name)):
                print("Download successful")
                #blob_old = srcbucket.blob(blob.name)
                #blob_new = srcbucket.copy_blob(blob_old, dstbucket, new_name=blob_old.name)
                #print(blob_new)
                #blob_old.delete()
            else:
                print("Download failed")

prefixes = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]

if __name__ == "__main__":
    for i in prefixes:
        x = Thread(target=download_thread, args=(i,))
        x.start()