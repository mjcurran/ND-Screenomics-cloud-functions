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

## Publishing file watcher

Open the Google Cloud Shell Terminal under your project.  
Create a folder called watcher in the terminal and cd into it.
Create a file, main.py, copy the code from ./watcher/main.py into it and save.  
   
Then run the following in the terminal in your watcher folder.  

```
gcloud functions deploy your-function-name \
--gen2 \
--runtime=python310 \
--region=us-central1 \
--source=. \
--entry-point=decrypt_and_move \
--trigger-event-filters="type=google.cloud.storage.object.v1.finalized" \
--trigger-event-filters="bucket=your-source-bucket"
```