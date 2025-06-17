"""
Save and load models, preprocessors
"""
import os
import pickle
from google.cloud import storage
from titanic.params import MODEL_FOLDER, BUCKET_NAME


def save_model(model, path: str, cloud: bool = False):
    """
    Save a model to the specified path.
    
    Args:
        model: The model to save.
        path (str): The file path where the model will be saved.
        cloud (bool): Whether to save the model to the cloud.
    """
    final_path = os.path.join(MODEL_FOLDER, path)
    with open(final_path, 'wb') as f:
        pickle.dump(model, f)
    if cloud:
        upload_blob(
            bucket_name=BUCKET_NAME,
            source_file_name=final_path,
            destination_blob_name=path
        )
        print(f"✅ Model saved to cloud from {final_path} to {BUCKET_NAME}/{path}")

def load_model(path: str, cloud: bool = False):
    """
    Load a model from the specified path.
    
    Args:
        path (str): The file path from which the model will be loaded.
        
    Returns:
        The loaded model.
    """
    if not os.path.exists(MODEL_FOLDER):
        os.makedirs(MODEL_FOLDER)
    if cloud : 
        download_blob(
            bucket_name=BUCKET_NAME,
            source_blob_name=path,
            destination_file_name=os.path.join(MODEL_FOLDER, path)
        )
        print(f"✅ Model downloaded from cloud to {os.path.join(MODEL_FOLDER, path)}")
    final_path = os.path.join(MODEL_FOLDER, path)
    with open(final_path, 'rb') as f:
        model = pickle.load(f)
    return model


def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)

    print(
        f"✅ Blob {source_blob_name} downloaded to {destination_file_name}."
    )


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)

    print(
        f"✅ File {source_file_name} uploaded to {destination_blob_name}."
    )