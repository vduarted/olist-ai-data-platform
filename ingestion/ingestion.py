import kagglehub
import boto3
from pathlib import Path
from datetime import date

AWS_PROFILE = "olist-tf"
S3_BUCKET = "olist-landing"
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
INGESTION_DATE = date.today()

session = boto3.Session(profile_name=AWS_PROFILE)
s3 = session.client("s3")

def data_download():
    return kagglehub.dataset_download("olistbr/brazilian-ecommerce", output_dir=str(DATA_DIR))

def data_upload(file_path:str, key:str):
    s3.upload_file(Filename=file_path, Key=key, Bucket=S3_BUCKET)

if __name__ == "__main__":
    data_download()
    files = list(DATA_DIR.glob("*.csv"))
    total_files = len(files)
    sent_files = 0

    if total_files == 0:
        raise FileNotFoundError("No files to upload. Check the source folder")

    for file in files:
        table_name = file.stem.removeprefix("olist_").removesuffix("_dataset")
        key = f"{table_name}/ingestion_date={INGESTION_DATE}/{file.name}"

        data_upload(file_path=str(file), key=key)
        sent_files += 1
        print(f"Uploaded file in {key}. Step: {sent_files}/{total_files}")