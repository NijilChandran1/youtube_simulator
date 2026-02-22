from google.cloud import storage

def upload_file(bucket_name, destination_blob_name, file_to_be_uploaded):
    # Initialize a client
    storage_client = storage.Client()

    # Get the bucket
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(file_to_be_uploaded)

    print(f"File {destination_blob_name} uploaded to {bucket_name}.")


bucket_name = 'alphabet_tsr'
destination_blob_name = 'videos/simulator/superbowl-2026.mp4'
file_to_be_uploaded="C:\\Users\\NijilChandran\\workspace\\transformation\\youtube_simulator\\frontend\\public\\assets\\superbowl-2026.mp4"
upload_file(bucket_name, destination_blob_name,file_to_be_uploaded)

