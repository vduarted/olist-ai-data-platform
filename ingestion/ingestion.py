import kagglehub
import boto3
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

def data_download():
    return kagglehub.dataset_download("olistbr/brazilian-ecommerce", output_dir=str(DATA_DIR))

if __name__ == "__main__":
    data_download()