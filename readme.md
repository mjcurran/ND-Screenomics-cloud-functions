# ScreenLife Capture Cloud Functions

This repo contains the cloud functions used during the ScreenLife Capture study.

## Functions

**register** 

```
POST {
	"username": string,
	"key": string
}
Responses
- 201 Created
- 405 Invalid method (only POST)
- 409 User already exists
```

**upload_file** 

```
POST {
	"username": string,
	"key": string
}
(include images to upload under `files`)
Responses
- 201 Successfully Uploaded
- 404 Invalid username/key
- 405 Invalid method (only POST)
```

**count_files**

```
POST {
	"username": string,
	"key": string,
	"fileNames": string[]
}
Responses
- 200 All files verified
- 400 Files missed, list of missed files under `missedPictures`
- 404 Invalid username/key
- 405 Invalid method (only POST)
```
  

# University of Notre Dame Changes  
  
## Second bucket for decryption in cloud
In main.py in the root folcder, set BUCKET_NAME to your primary upload bucket.  
Set SECOND_BUCKET_NAME to one you will use for a source to decrypt the images from.  The file watcher function will monitor this second bucket, and decrypt the files as they come in, and save to another secure bucket.
```
PROJECT_ID = "time-screenlife-capture"
BUCKET_NAME = "notre-dame-screenomics"
SECOND_BUCKET_NAME = "staged-screenomics"
```
## Publishing file watcher

Open the Google Cloud Shell Terminal under your project.  
Create a folder called watcher in the terminal and cd into it.
Create a file, main.py, copy the code from ./watcher/main.py into it and save.  
Create a file called requirements.txt in the same filder and copy the contents from watcher/requirements.txt into it.
   
Then run the following in the terminal in your watcher folder.  

```
gcloud functions deploy copy-func \
--gen2 \
--runtime=python310 \
--region=us-central1 \
--source=. \
--entry-point=decrypt_and_move \
--trigger-event-filters="type=google.cloud.storage.object.v1.finalized" \
--trigger-event-filters="bucket=staged-screenomics"
```
In this example the function will be named "copy-func", and then bucket that it watches is called "staged-screenomics".  
"decrypt_and_move" is the name of the main function in /watcher/main.py  

## Utilities for adcvanced users
In the utils folder are some command line tools to help in certain situations.  
`bulk_decrypt.py` : This is a tool for use on the Google Cloud console.  It will try to decrypt all the files in one bucket into another bucket based on the keyfile name.  Because of the huge number of files the Screenomics app creates, this process will time-out and stop after about 8-12 hours, so the keyfile name and other matching criteria should be edited before each run to take batches of files per run.
  
`multithreaded_downloader.py` is a function meant to be run on a local computer or server where you want to download all the decrypted files.  It will spawn up to 16 threads to work simultaneously to speed up the process. The GCloud API client is required to be installed before you can run this.  

Before running set the following in the file:
```
data_folder = "/home/youruser/gcloud"  # where you want the files downloaded to
key_path = "/home/youruser/gcloud/bucket_key.json"  # the path to your GCloud keys file 

SRC_BUCKET_NAME = "final-screenomics"  # your decrypted image bucket name
```
