from google.cloud import storage
from google.cloud.storage import Blob
from Crypto.Cipher import AES
import hashlib

PROJECT_ID = "time-screenlife-capture"
SRC_BUCKET_NAME = "notre-dame-screenomics"
#SRC_BUCKET_NAME = "staged-screenomics"
DST_BUCKET_NAME = "final-screenomics"
KEY_BUCKET_NAME = "screenomics-keystore"

client = storage.Client(project=PROJECT_ID)
src_bucket = client.get_bucket(SRC_BUCKET_NAME)
dst_bucket = client.get_bucket(DST_BUCKET_NAME)
key_bucket = client.get_bucket(KEY_BUCKET_NAME)

def decrypt_image(file, key):
    fileparts = file.split('/')
    filename = fileparts[1]
    new_blob = dst_bucket.blob(file)
    if not new_blob.exists():
        h = hashlib.sha256(filename.encode())
        newiv = bytes.fromhex(h.hexdigest())
        iv = newiv[:7]
        bytekey = bytes.fromhex(key)
        cipher = AES.new(bytekey, AES.MODE_GCM, nonce=iv)
        blob = src_bucket.blob(file)
        with blob.open("rb") as f:
            contents = f.read()
        decrypted_data = cipher.decrypt(contents)
        new_blob = dst_bucket.blob(file)
        with new_blob.open("wb") as w:
            w.write(decrypted_data)

def main():
    keys = client.list_blobs(KEY_BUCKET_NAME)

    for keyfile in keys:
        if keyfile.name == "87ea235a":
            blobs = client.list_blobs(SRC_BUCKET_NAME, prefix=keyfile.name + "/2023_01")
            with keyfile.open('r') as f:
                key = f.read()
            print(key)
            for blob in blobs:
                print(blob.name)
                decrypt_image(blob.name, key)


main()