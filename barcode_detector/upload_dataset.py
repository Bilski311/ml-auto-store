from azureml.core import Workspace
from azure.core.exceptions import ResourceExistsError
from config import storage_account_key, storage_account_name, container_name

from azure.storage.blob import BlobServiceClient
import os
import time


def delete_container(container_client):
    try:
        container_client.delete_container()
        print("Container deleted successfully.")
    except Exception as e:
        print("Container could not be deleted or does not exist. Error:", e)


def recreate_storage_container(container_client):
    delete_container(container_client)
    max_retries = 20
    for _ in range(max_retries):
        try:
            blob_service_client.create_container(container_name)
            print("Container created.")
            return
        except ResourceExistsError:
            print("Container is being deleted. Waiting before retrying...")
            time.sleep(5)

    print("Failed to create container after retrying. Exiting.")
    exit(1)


def create_blob_service_client():
    connection_string = f"DefaultEndpointsProtocol=https;AccountName={storage_account_name};AccountKey={storage_account_key};EndpointSuffix=core.windows.net"

    return BlobServiceClient.from_connection_string(connection_string)


def upload_specific_directories(directory_to_upload, subdirectories):
    for subdirectory in subdirectories:
        full_subdirectory_path = os.path.join(directory_to_upload, subdirectory)
        if not os.path.exists(full_subdirectory_path):
            print(f"Subdirectory {subdirectory} does not exist.")
            continue
        for filename in sorted(os.listdir(full_subdirectory_path)):
            if os.path.isfile(os.path.join(full_subdirectory_path, filename)):
                file_path = os.path.join(full_subdirectory_path, filename)
                blob_name = os.path.join(subdirectory, filename)
                blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
                with open(file_path, "rb") as data:
                    blob_client.upload_blob(data, overwrite=True)
                print(f"Uploaded {file_path} to blob {blob_name}.")


if __name__ == '__main__':
    recreate = True
    ws = Workspace.from_config()
    blob_service_client = create_blob_service_client()
    container_client = blob_service_client.get_container_client(container=container_name)
    if recreate: recreate_storage_container(container_client)

    file_to_upload = 'test.txt'
    blob_name = os.path.basename(file_to_upload)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    directory_to_upload = '../dataset'
    subdirectories_to_upload = ['images', 'labels']
    upload_specific_directories(directory_to_upload, subdirectories_to_upload)
