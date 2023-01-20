"""
Cloud function to decrypt images as they are saved and copy them to a different bucket
* update original HTTP POST function to store to second bucket, add trigger function on that
bucket to decrypt in place.

gcloud functions deploy test-copy-func \
--gen2 \
--runtime=python310 \
--region=us-central1 \
--source=. \
--entry-point=test_decrypt_and_move \
--trigger-event-filters="type=google.cloud.storage.object.v1.finalized" \
--trigger-event-filters="bucket=staged-screenomics"

"""

import functions_framework
from google.cloud import storage
from google.cloud.storage import Blob
from Crypto.Cipher import AES
import hashlib

PROJECT_ID = "time-screenlife-capture"
#SRC_BUCKET_NAME = "dev-nd-screenomics"
SRC_BUCKET_NAME = "staged-screenomics"
DST_BUCKET_NAME = "final-screenomics"
KEY_BUCKET_NAME = "screenomics-keystore"

client = storage.Client(project=PROJECT_ID)
src_bucket = client.get_bucket(SRC_BUCKET_NAME)
dst_bucket = client.get_bucket(DST_BUCKET_NAME)
key_bucket = client.get_bucket(KEY_BUCKET_NAME)

def decrypt_image(file, key):
    fileparts = file.split('/')
    filename = fileparts[1]
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

# Triggered by a change in a storage bucket
@functions_framework.cloud_event
def test_decrypt_and_move(cloud_event):
    data = cloud_event.data

    event_id = cloud_event["id"]
    event_type = cloud_event["type"]

    bucket = data["bucket"]
    filename = data["name"]
    metageneration = data["metageneration"]
    timeCreated = data["timeCreated"]
    updated = data["updated"]

    print(f"Event ID: {event_id}")
    print(f"Event type: {event_type}")
    print(f"Bucket: {bucket}")
    print(f"File: {filename}")
    print(f"Metageneration: {metageneration}")
    print(f"Created: {timeCreated}")
    print(f"Updated: {updated}")

    # find the key, if it exists
    fileparts = filename.split('/')
    user = fileparts[0]
    #blob = key_bucket.blob(user)
    blobs = client.list_blobs(KEY_BUCKET_NAME)

    for blob in blobs:
        if blob.name == user:
            # found key
            with blob.open("r") as f:
                key = f.read()
            decrypt_image(filename, key)
            