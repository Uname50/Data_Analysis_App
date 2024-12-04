import pandas as pd
from pathlib import Path
from google.cloud import storage

def process_uploaded_file(file_path: Path) -> dict:
    
    """
    Process an uploaded file to clean and transform data
    """

    # Determine the file type and turn it into a Pandas DataFrame
    if file_path.suffix == ".csv":
        df = pd.read_csv(file_path)
    elif file_path.suffix == ".json":
        df = pd.read_json(file_path)
    else:
        raise ValueError("Unsupported file type, only CSV or JSON files are allowed")
    
    # Fill missing values with 0
    df.fillna(0, inplace=True)

    # Test operation: combine to create sales by category
    if "category" in df.columns and "sales" in df.columns:
        sales_by_category = df.groupby("category")["sales"].sum().reset_index()
        return {"sales_by_category": sales_by_category.to_dict(orient="records")}
    else:
        return{"message": "Required columns are not found in the DF"}

def upload_to_gcs(bucket_name: str, source_file_path: Path, destination_blob_name: str):
    
    """
    Uploads file to Google Cloud Storage
    """

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Upload the file
    blob.upload_from_filename(str(source_file_path))

    return blob.public_url

def save_and_upload_processed_data(df: pd.DataFrame, output_file_path: Path, bucket_name: str):

    """
    Save the processed DF into a CSV file and upload it to GCS
    """

    # Save the DF to CSV
    df.to_csv(output_file_path, index=False)

    # Upload the CSV
    file_name = output_file_path.name
    gcs_url = upload_to_gcs(bucket_name, output_file_path, file_name)

    return gcs_url

