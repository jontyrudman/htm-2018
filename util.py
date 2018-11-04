from google.cloud import storage

def upload_blob(bucket_name, source_file_name, destination_blob_name):
  """Uploads a file to the bucket."""
  storage_client = storage.Client()
  if file_exists(bucket_name, source_file_name):
      return
  bucket = storage_client.get_bucket(bucket_name)
  blob = bucket.blob(destination_blob_name)

  blob.upload_from_filename(source_file_name)

  print('File {} uploaded to {}.'.format(
      source_file_name,
      destination_blob_name))

def file_exists(*args):
    if len(args) == 2 and isinstance(args[0], str) and isinstance(args[1], str):
        filepath = "gs://{}/{}".format(args[0], args[1])
    if len(args) == 1 and isinstance(args[0], str):
        try:
            gcs.stat(filepath)
            return true
        except gcs_errors.NotFoundError as e:
            return false

def list_blobs(bucket_name):
    """Lists all the blobs in the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)

    blobs = bucket.list_blobs()

    for blob in blobs:
        yield blob
