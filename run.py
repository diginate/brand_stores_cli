import argparse
import os
import subprocess
import csv
from datetime import datetime

try:
    import boto3
    from botocore.exceptions import NoCredentialsError
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Error: Required libraries are not installed. Please run: pip install boto3 python-dotenv")
    exit(1)

# --- Configuration ---
ARTWORK_MASTER_FOLDER = "/Volumes/Seagate Tim /DROPBOX/Diginate Dropbox/Tim Lamm/OTHER/CUSTOMSKINS STUFF/BRAND STORE"
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "csbrandstores")
LOG_FILE = "creation_log.csv"

def upload_folder_to_s3(folder_path, s3_bucket, s3_folder):
    """
    Uploads the contents of a folder to an S3 bucket.
    """
    print(f"Starting upload of folder '{folder_path}' to S3 bucket '{s3_bucket}'...")
    s3_client = boto3.client('s3')
    try:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                local_path = os.path.join(root, file)
                relative_path = os.path.relpath(local_path, folder_path)
                s3_key = os.path.join(s3_folder, relative_path)
                
                print(f"  Uploading {local_path} to s3://{s3_bucket}/{s3_key}")
                s3_client.upload_file(local_path, s3_bucket, s3_key)
        print("Upload successful.")
        return True
    except FileNotFoundError:
        print(f"  ERROR: Local folder not found: {folder_path}")
        return False
    except NoCredentialsError:
        print("  ERROR: AWS credentials not found. Please configure them (e.g., in ~/.aws/credentials or as environment variables).")
        return False
    except Exception as e:
        print(f"  An unexpected error occurred during S3 upload: {e}")
        return False

def run_product_creation(product_id):
    """
    Runs the shell scripts to create all Shopify products.
    """
    print(f"Starting product creation for ID: {product_id}...")
    scripts_to_run = [
        './create_all_colors.sh',
        './create_all_stickers.sh',
        './create_hoodies.sh',
        './create_misc_items.sh'
    ]
    
    all_successful = True
    for script in scripts_to_run:
        print(f"  Running {script}...")
        try:
            # Using subprocess.run for simplicity and better error handling
            result = subprocess.run(
                [script, str(product_id)],
                capture_output=True,
                text=True,
                check=True  # This will raise a CalledProcessError if the script returns a non-zero exit code
            )
            print(f"  --- Script output ---")
            print(result.stdout)
            print(f"  --- End script output ---")
            print(f"  {script} completed successfully.")
        except FileNotFoundError:
            print(f"  ERROR: Script not found: {script}. Make sure it's in the same directory and has execute permissions.")
            all_successful = False
        except subprocess.CalledProcessError as e:
            print(f"  ERROR running script {script}. It returned a non-zero exit code.")
            print(f"  --- STDERR ---")
            print(e.stderr)
            print(f"  --- STDOUT ---")
            print(e.stdout)
            print(f"  --- End error output ---")
            all_successful = False
        except Exception as e:
            print(f"  An unexpected error occurred while running {script}: {e}")
            all_successful = False
            
    if all_successful:
        print("All product creation scripts ran successfully.")
        return True
    else:
        print("One or more product creation scripts failed.")
        return False

def log_to_csv(log_data):
    """
    Appends a log entry to the CSV file.
    """
    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, 'a', newline='') as csvfile:
        fieldnames = ['timestamp', 'id', 's3_upload_status', 'product_creation_status']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
        
        writer.writerow(log_data)

def main():
    parser = argparse.ArgumentParser(description="Uploads artwork to S3 and creates Shopify products.")
    parser.add_argument("product_id", help="The ID for the artwork and products.")
    args = parser.parse_args()
    
    product_id = args.product_id
    
    # Construct the path to the artwork previews folder
    artwork_previews_path = os.path.join(ARTWORK_MASTER_FOLDER, product_id, '_previews')
    
    # --- Step 1: Upload to S3 ---
    s3_folder_key = f"{product_id}/_previews"
    s3_success = upload_folder_to_s3(artwork_previews_path, S3_BUCKET_NAME, s3_folder_key)
    
    # --- Step 2: Create Products on Shopify ---
    product_creation_success = False
    if s3_success:
        product_creation_success = run_product_creation(product_id)
    else:
        print("Skipping product creation due to S3 upload failure.")
        
    # --- Step 3: Log the outcome ---
    log_data = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'id': product_id,
        's3_upload_status': 'Success' if s3_success else 'Failure',
        'product_creation_status': 'Success' if product_creation_success else 'Failure'
    }
    log_to_csv(log_data)
    
    print("\nProcess finished.")
    print(f"  - S3 Upload: {'Success' if s3_success else 'Failure'}")
    print(f"  - Product Creation: {'Success' if product_creation_success else 'Failure'}")
    print(f"Results have been logged to {LOG_FILE}")

if __name__ == "__main__":
    main()
