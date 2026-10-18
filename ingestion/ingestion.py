import kagglehub
import boto3
from pathlib import Path

def data_download():
    data_dir = Path(__file__).resolve().parent.parent / "data"
    return kagglehub.dataset_download("olistbr/brazilian-ecommerce", output_dir=data_dir)

if __name__ == "__main__":
    data_download()