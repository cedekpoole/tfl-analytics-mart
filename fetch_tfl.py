import json
import os
import requests
from datetime import datetime, timezone
import argparse
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import AzureError

# the TfL API endpoint for London Underground tube line statuses
URL = "https://api.tfl.gov.uk/Line/Mode/tube/Status"
# set the folder path where the file will be saved
OUTPUT_DIR = "data/raw/tfl"

# azure storage info
STORAGE_ACCOUNT_NAME = "tflanalyticsmartcp"
CONTAINER_NAME = "raw-tfl"
ACCOUNT_URL = f"https://{STORAGE_ACCOUNT_NAME}.blob.core.windows.net"


def get_tfl_data():
    response = requests.get(URL, timeout=30)
    # if the API returned error (e.g. 404, 500), script will stop and print error message
    response.raise_for_status()
    return response.json()


def validate_tfl_data(data):
    # if data from response is empty, raise a value error
    if not data:
        raise ValueError("The TfL API returned no data")

    # validate the shape of each response line
    for line in data:
        if "name" not in line:
            raise ValueError("TfL line is missing name")
        if "lineStatuses" not in line or not line["lineStatuses"]:
            raise ValueError("TfL line missing line status data")
        if "statusSeverityDescription" not in line["lineStatuses"][0]:
            raise ValueError("TfL line status is missing description")


# add metadata to the saved JSON file
def build_output_payload(data):
    utc_fetched_at = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")

    return {"utc_fetched_at": utc_fetched_at, "source_url": URL, "data": data}


def save_tfl_payload(data, output_dir=OUTPUT_DIR):
    # create the output directory folder if it doesn't exist yet
    os.makedirs(output_dir, exist_ok=True)

    # build a filename using the current date and time so each file is unique
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"tfl_lines_{timestamp}.json"
    # create full file path e.g. "data/raw/tfl/tfl_lines_2026-06-20_14-30-00.json"
    output_path = os.path.join(output_dir, filename)

    payload = build_output_payload(data)

    # open the file for writing and save the data as formatted JSON
    with open(output_path, "w") as f:
        json.dump(payload, f, indent=2)

    return output_path


# upload tfl data to azure
def upload_to_blob(file_path):
    # use the Azure account currently signed in through "az login"
    credential = DefaultAzureCredential()

    # connect to storage account
    blob_service_client = BlobServiceClient(
        account_url=ACCOUNT_URL,
        credential=credential,
    )

    # get only the filename from the full local path
    # e.g. "data/raw/tfl/example.json" becomes "example.json"
    blob_name = os.path.basename(file_path)

    # point to the filename inside the raw-tfl container
    blob_client = blob_service_client.get_blob_client(
        container=CONTAINER_NAME,
        blob=blob_name,
    )

    # open the local file as binary data and upload it (rb = bytes)
    with open(file_path, "rb") as file:
        blob_client.upload_blob(file, overwrite=False)

    return blob_name


def print_line_statuses(data):
    # always check the shape of the tfl data first
    # function prints status to terminal
    for line in data:
        name = line["name"]
        status = line["lineStatuses"][0]["statusSeverityDescription"]
        print(f"{name} : {status}")


# allow users to pick output folder path if needed
def parse_args():
    parser = argparse.ArgumentParser(description="Fetch TfL tube line status data")
    parser.add_argument(
        "--output-dir", default=OUTPUT_DIR, help="Folder where JSON file will be saved"
    )
    return parser.parse_args()


def main():
    args = parse_args()

    try:
        data = get_tfl_data()
        validate_tfl_data(data)
        print_line_statuses(data)
        output_path = save_tfl_payload(data, output_dir=args.output_dir)
        print(f"Saved {len(data)} lines to {output_path}")
        blob_name = upload_to_blob(output_path)
        print(f"Uploaded {blob_name} to Azure Blob Storage")
    except requests.exceptions.RequestException as error:
        print(f"Error fetching TfL data: {error}")
    except ValueError as error:
        print(f"Invalid data: {error}")
    except AzureError as error:
        print(f"Error loading to blob storage: {error}")


if __name__ == "__main__":
    main()
