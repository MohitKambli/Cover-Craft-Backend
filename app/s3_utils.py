import boto3
from werkzeug.utils import secure_filename
from app.config import Config

# Initialize S3 client
s3_client = boto3.client(
    "s3",
    region_name=Config.AWS_REGION,
    aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
)

def upload_file_to_s3(file, folder="resumes/"):
    """
    Uploads a file to an S3 bucket and returns the S3 key and public URL.
    :param file: File object to be uploaded
    :param folder: Folder path in S3 bucket
    :return: S3 key (path) and pre-signed URL
    """
    try:
        # Secure the file name
        filename = secure_filename(file.filename)
        s3_key = f"{folder}{filename}"

        # Upload file to S3
        s3_client.upload_fileobj(file, Config.AWS_S3_BUCKET_NAME, s3_key)

        # Generate pre-signed URL
        pre_signed_url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": Config.AWS_S3_BUCKET_NAME, "Key": s3_key},
            ExpiresIn=1800,  # URL valid for 30 mins
        )

        return s3_key, pre_signed_url

    except Exception as e:
        raise RuntimeError(f"Failed to upload file to S3: {e}")
