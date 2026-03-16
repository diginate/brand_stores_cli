#!/usr/bin/env python3
import boto3
import os
import sys
import argparse
import mimetypes
from botocore.exceptions import NoCredentialsError, ClientError

# Configuration
# These will be loaded from environment when the module is imported
# Make sure load_dotenv() is called before using these defaults if relying on .env
BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "csbrandstores")
REGION = os.getenv("AWS_DEFAULT_REGION", "eu-north-1")

def upload_directory_to_s3(product_id, local_directory, bucket_name=None, region=None):
    """
    Uploads all files in a local directory to S3 under the path:
    {product_id}/_previews/{filename}
    
    Returns:
        tuple: (success (bool), message (str), count (int))
    """
    
    target_bucket = bucket_name or BUCKET_NAME
    target_region = region or REGION
    
    # Initialize S3 client
    try:
        s3 = boto3.client('s3', region_name=target_region)
    except Exception as e:
        return False, f"Failed to initialize S3 client: {e}", 0
    
    # Check if directory exists
    if not os.path.isdir(local_directory):
        return False, f"Directory '{local_directory}' does not exist.", 0
        
    # Check if the directory structure matches the expected format (Product ID -> _previews)
    # If the user points to a parent folder that contains the Product ID folder
    potential_product_dir = os.path.join(local_directory, product_id)
    if os.path.isdir(potential_product_dir):
        print(f"Found product directory inside: {potential_product_dir}")
        local_directory = potential_product_dir
        
    # If the user points to the Product ID folder itself, check for _previews
    potential_previews_dir = os.path.join(local_directory, "_previews")
    if os.path.isdir(potential_previews_dir):
        print(f"Found _previews directory inside: {potential_previews_dir}")
        local_directory = potential_previews_dir
    
    print(f"Starting upload for Product ID: {product_id}")
    print(f"Source Directory: {local_directory}")
    print(f"Target Bucket: {target_bucket}")
    print("-" * 40)

    files_uploaded = 0
    
    try:
        # Iterate through files in the directory
        for filename in os.listdir(local_directory):
            file_path = os.path.join(local_directory, filename)
            
            # Skip directories and hidden files
            if os.path.isfile(file_path) and not filename.startswith('.'):
                
                # Construct S3 key (path)
                # The app expects images at: https://csbrandstore.s3.eu-central-1.amazonaws.com/{id}/_previews/{filename}
                s3_key = f"{product_id}/_previews/{filename}"
                
                # Guess content type based on file extension
                content_type, _ = mimetypes.guess_type(file_path)
                if content_type is None:
                    content_type = 'application/octet-stream'
                
                print(f"Uploading {filename} to s3://{target_bucket}/{s3_key}...")
                
                # Upload file
                s3.upload_file(
                    file_path, 
                    target_bucket, 
                    s3_key, 
                    ExtraArgs={'ContentType': content_type}
                )
                files_uploaded += 1
                
        print("-" * 40)
        if files_uploaded == 0:
            return True, "Warning: No files were found to upload.", 0
        else:
            msg = f"Successfully uploaded {files_uploaded} files."
            print(msg)
            print(f"Images should be accessible at: https://{target_bucket}.s3.{target_region}.amazonaws.com/{product_id}/_previews/<filename>")
            return True, msg, files_uploaded

    except NoCredentialsError:
        return False, "Error: AWS credentials not found.", 0
    except ClientError as e:
        return False, f"AWS Error: {e}", 0
    except Exception as e:
        return False, f"Unexpected error: {e}", 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload product images to S3 for Shopify CLI App")
    parser.add_argument("product_id", help="The Product ID (e.g., 7822589100186B)")
    parser.add_argument("directory", help="Path to the local directory containing images")
    
    args = parser.parse_args()
    
    success, message, count = upload_directory_to_s3(args.product_id, args.directory)
    if not success:
        print(message)
        sys.exit(1)
    else:
        print(message)
        sys.exit(0)
