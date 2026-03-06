#!/usr/bin/env python3
import boto3
import os
import sys
import argparse
import mimetypes
from botocore.exceptions import NoCredentialsError, ClientError

# Configuration
BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "csbrandstores")
REGION = os.getenv("AWS_DEFAULT_REGION", "eu-north-1")

def upload_directory_to_s3(product_id, local_directory):
    """
    Uploads all files in a local directory to S3 under the path:
    {product_id}/_previews/{filename}
    """
    
    # Initialize S3 client
    s3 = boto3.client('s3', region_name=REGION)
    
    # Check if directory exists
    if not os.path.isdir(local_directory):
        print(f"Error: Directory '{local_directory}' does not exist.")
        sys.exit(1)
        
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
    print(f"Target Bucket: {BUCKET_NAME}")
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
                
                print(f"Uploading {filename} to s3://{BUCKET_NAME}/{s3_key}...")
                
                # Upload file
                s3.upload_file(
                    file_path, 
                    BUCKET_NAME, 
                    s3_key, 
                    ExtraArgs={'ContentType': content_type}
                )
                files_uploaded += 1
                
        print("-" * 40)
        if files_uploaded == 0:
            print("Warning: No files were found to upload.")
        else:
            print(f"Successfully uploaded {files_uploaded} files.")
            print(f"Images should be accessible at: https://{BUCKET_NAME}.s3.{REGION}.amazonaws.com/{product_id}/_previews/<filename>")

    except NoCredentialsError:
        print("Error: AWS credentials not found.")
        print("Please configure your credentials using one of the following methods:")
        print("1. Set environment variables: AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY")
        print("2. Run 'aws configure' if you have the AWS CLI installed")
        print("3. Create a ~/.aws/credentials file")
        sys.exit(1)
    except ClientError as e:
        print(f"AWS Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload product images to S3 for Shopify CLI App")
    parser.add_argument("product_id", help="The Product ID (e.g., 7822589100186B)")
    parser.add_argument("directory", help="Path to the local directory containing images")
    
    args = parser.parse_args()
    
    upload_directory_to_s3(args.product_id, args.directory)
