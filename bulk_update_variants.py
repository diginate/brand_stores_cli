#!/usr/bin/env python3
import shopify
import os
import argparse
import json
import time
import requests
import csv
import math
import shutil
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Shopify Credentials (ensure these are correct for your private app) ---
# It's recommended to use environment variables for these in a real application
API_KEY = os.getenv("SHOPIFY_API_KEY")
PASSWORD = os.getenv("SHOPIFY_PASSWORD")
SHOP_NAME = os.getenv("SHOPIFY_SHOP_NAME")
API_VERSION = os.getenv("SHOPIFY_API_VERSION", "2024-04")
# The number of variants to include in each smaller file sent to Shopify.
# Shopify has a file size limit for bulk operations (around 100-250MB).
# 10,000 variants per file is a safe number to stay well under this limit.
CHUNK_SIZE = 10000 

# --- GraphQL Queries and Mutations ---
CREATE_STAGED_UPLOAD_MUTATION = """
mutation stagedUploadsCreate($input: [StagedUploadInput!]!) {
  stagedUploadsCreate(input: $input) {
    stagedTargets {
      url
      resourceUrl
      parameters {
        name
        value
      }
    }
    userErrors {
      field
      message
    }
  }
}
"""

BULK_OPERATION_RUN_MUTATION = """
mutation bulkOperationRunMutation($mutation: String!, $stagedUploadPath: String!) {
  bulkOperationRunMutation(mutation: $mutation, stagedUploadPath: $stagedUploadPath) {
    bulkOperation {
      id
      status
    }
    userErrors {
      field
      message
    }
  }
}
"""

GET_BULK_OPERATION_STATUS_BY_ID_QUERY = """
query getBulkOperationStatus($id: ID!) {
  node(id: $id) {
    ... on BulkOperation {
      id
      status
      errorCode
      createdAt
      completedAt
      objectCount
      fileSize
      url
      partialDataUrl
    }
  }
}
"""

GET_CURRENT_BULK_OPERATION_QUERY = """
query {
  currentBulkOperation {
    id
    status
    errorCode
    createdAt
    completedAt
    objectCount
    fileSize
    url
    partialDataUrl
  }
}
"""

# This is the actual mutation that will be run for each line in the uploaded file.
PRODUCT_VARIANT_UPDATE_MUTATION = """
mutation productVariantUpdate($input: ProductVariantInput!) {
  productVariantUpdate(input: $input) {
    productVariant {
      id
      price
    }
    userErrors {
      field
      message
    }
  }
}
"""

def setup_shopify_session():
    """Initializes the Shopify API session and returns a GraphQL client."""
    try:
        shop_url = f"https://{API_KEY}:{PASSWORD}@{SHOP_NAME}.myshopify.com/admin"
        # The ShopifyAPI library uses pyactiveresource, which needs the session configured this way.
        session = shopify.Session(shop_url, API_VERSION, PASSWORD)
        shopify.ShopifyResource.activate_session(session)
        print("Shopify session activated.")
        # The GraphQL client uses the activated session.
        return shopify.GraphQL()
    except Exception as e:
        print(f"Error activating Shopify session: {e}")
        return None

def generate_jsonl_from_csv(csv_path, jsonl_path):
    """Reads a CSV and generates a JSONL file for the bulk mutation."""
    print(f"Generating JSONL file from {csv_path}...")
    count = 0
    try:
        with open(csv_path, mode='r', encoding='utf-8') as csv_file, \
             open(jsonl_path, mode='w', encoding='utf-8') as jsonl_file:
            csv_reader = csv.reader(csv_file)
            header = next(csv_reader)  # Read header
            
            # Find column indices, making it robust to column order.
            try:
                variant_gid_idx = header.index('variant_gid')
                price_idx = header.index('price')
            except ValueError as e:
                print(f"ERROR: CSV header is missing required column. Missing: {e}. Header found: {header}")
                return False

            for row in csv_reader:
                variant_gid = row[variant_gid_idx]
                price = row[price_idx]
                
                # Basic validation.
                if not variant_gid.startswith("gid://shopify/ProductVariant/"):
                    print(f"WARNING: Skipping invalid variant GID format: {variant_gid}")
                    continue

                # Each line in the JSONL file corresponds to the variables for one mutation call.
                mutation_vars = {
                    "input": {
                        "id": variant_gid,
                        "price": price
                    }
                }
                jsonl_file.write(json.dumps(mutation_vars) + '\n')
                count += 1
        print(f"Generated {count} lines in {jsonl_path}.")
        return count > 0
    except FileNotFoundError:
        print(f"ERROR: Input CSV file not found at '{csv_path}'")
        return False
    except Exception as e:
        print(f"An error occurred during JSONL generation: {e}")
        return False


def create_staged_upload(graphql_client, jsonl_path):
    """Creates a staged upload target on Shopify to get a URL for uploading the data."""
    print("Requesting staged upload URL from Shopify...")
    filename = os.path.basename(jsonl_path)
    
    variables = {
        "input": [{
            "filename": filename,
            "mimeType": "application/jsonl",
            "resource": "BULK_MUTATION_VARIABLES",
            "httpMethod": "POST"
        }]
    }
    
    result_str = graphql_client.execute(CREATE_STAGED_UPLOAD_MUTATION, variables=variables)
    result = json.loads(result_str)

    user_errors = result.get("data", {}).get("stagedUploadsCreate", {}).get("userErrors", [])
    if user_errors:
        print(f"Error creating staged upload: {user_errors}")
        return None
    
    staged_target = result["data"]["stagedUploadsCreate"]["stagedTargets"][0]
    print("Successfully created staged upload target.")
    return staged_target

def upload_file_to_staged_url(staged_target, jsonl_path):
    """
    Uploads the JSONL file to the Shopify-provided signed URL.
    Returns the upload key required for the bulk mutation.
    """
    upload_url = staged_target['url']
    # The parameters from the staged upload response must be sent as form data.
    form_data = {param['name']: param['value'] for param in staged_target['parameters']}
    
    # The 'key' parameter is what Shopify uses as the stagedUploadPath for the bulk operation.
    upload_key = None
    for param in staged_target['parameters']:
        if param['name'] == 'key':
            upload_key = param['value']
            break

    if not upload_key:
        print("Error: Could not find 'key' parameter in staged upload target. Cannot start bulk operation.")
        return None
    
    print(f"Uploading {jsonl_path} to Shopify's staged target...")
    with open(jsonl_path, 'rb') as f:
        # The file content itself is sent as the 'file' part of the multipart form.
        files = {'file': f}
        response = requests.post(upload_url, data=form_data, files=files)

    if response.status_code == 201:
        print("File uploaded successfully.")
        # Return the key, which is the path Shopify needs.
        return upload_key
    else:
        print(f"Error uploading file: {response.status_code} - {response.text}")
        return None

def run_bulk_mutation(graphql_client, staged_upload_path):
    """Starts the bulk mutation operation on Shopify using the uploaded file path (key)."""
    print("Starting bulk mutation operation...")
    variables = {
        "mutation": PRODUCT_VARIANT_UPDATE_MUTATION,
        "stagedUploadPath": staged_upload_path
    }
    result_str = graphql_client.execute(BULK_OPERATION_RUN_MUTATION, variables=variables)
    result = json.loads(result_str)

    user_errors = result.get("data", {}).get("bulkOperationRunMutation", {}).get("userErrors", [])
    if user_errors:
        print(f"Error running bulk mutation: {user_errors}")
        return None
        
    bulk_operation = result["data"]["bulkOperationRunMutation"]["bulkOperation"]
    print(f"Bulk operation started: ID={bulk_operation['id']}, Status={bulk_operation['status']}")
    return bulk_operation

def poll_bulk_operation_status(graphql_client, operation_gid):
    """Polls Shopify for the completion of a specific bulk operation by its GID."""
    print(f"Polling for completion of bulk operation GID: {operation_gid}...")
    while True:
        # Give Shopify's servers a moment before the first poll.
        time.sleep(10)
        
        result_str = graphql_client.execute(GET_BULK_OPERATION_STATUS_BY_ID_QUERY, variables={"id": operation_gid})
        result = json.loads(result_str)
        operation = result.get("data", {}).get("node")

        if not operation:
            # This can happen right after creation; we just need to wait.
            print(f"  - Status: PENDING (at {time.ctime()}). Waiting for it to start...")
            continue

        status = operation['status']
        print(f"  - Status: {status} (at {time.ctime()})")

        if status in ['COMPLETED', 'FAILED', 'CANCELED', 'EXPIRED']:
            print(f"Bulk operation finished with status: {status}")
            return operation
        

def download_and_process_results(result_url):
    """Downloads and prints a summary of the results of the bulk operation."""
    if not result_url:
        print("No result URL provided. Cannot download results.")
        return

    print(f"Downloading results from: {result_url}")
    response = requests.get(result_url)
    if response.status_code != 200:
        print(f"Error downloading results: {response.status_code} - {response.text}")
        return

    print("\n--- Bulk Operation Results Summary ---")
    success_count = 0
    error_count = 0
    
    # The result from Shopify is a JSONL file.
    for line in response.iter_lines():
        if line:
            result_item = json.loads(line)
            # The result is nested under the 'data' key.
            update_result = result_item.get("data", {}).get("productVariantUpdate", {})
            if update_result:
                errors = update_result.get("userErrors")
                if errors:
                    error_count += 1
                    # Extract the ID from the input of the failed mutation for better logging.
                    # The response structure for errors does not consistently include the object ID.
                    # We look back at the original data that was sent.
                    original_input_id = result_item.get('__parentId') # This is a heuristic; might not always be present
                    print(f"ERROR: {errors} (Original Input ID context: {original_input_id})")
                else:
                    success_count += 1
            else: 
                # Check for top-level errors if the mutation itself failed to execute.
                item_errors = result_item.get("errors")
                if item_errors:
                    error_count += 1
                    print(f"TOP-LEVEL ERROR in result line: {item_errors}")

    print("\n--- Final Summary ---")
    print(f"Successful updates: {success_count}")
    print(f"Failed updates: {error_count}")
    print("---------------------\n")
    if error_count > 0:
        print("Review the errors above. The result file URL is valid for 7 days if you need to download it manually.")


def split_csv(input_file, temp_dir, chunk_size):
    """Splits a large CSV into smaller chunks in a temporary directory."""
    print(f"Splitting '{input_file}' into chunks of {chunk_size} rows...")
    try:
        with open(input_file, 'r', encoding='utf-8') as f_in:
            reader = csv.reader(f_in)
            header = next(reader)
            file_index = 0
            chunk_files = []

            while True:
                chunk_path = os.path.join(temp_dir, f"chunk_{file_index + 1}.csv")
                with open(chunk_path, 'w', newline='', encoding='utf-8') as f_out:
                    writer = csv.writer(f_out)
                    writer.writerow(header)
                    
                    # Read chunk_size rows
                    rows_written = 0
                    for i, row in enumerate(reader):
                        writer.writerow(row)
                        rows_written += 1
                        if rows_written >= chunk_size:
                            break
                    
                    if rows_written > 0:
                        chunk_files.append(chunk_path)
                        print(f"  - Created chunk: {chunk_path} ({rows_written} rows)")
                        file_index += 1
                    else:
                        # No more rows to read, break the loop
                        os.remove(chunk_path) # remove empty file
                        break
            
            print(f"Finished splitting into {len(chunk_files)} chunk(s).")
            return chunk_files

    except Exception as e:
        print(f"Error splitting CSV file: {e}")
        return []

def process_chunk(csv_path, chunk_num, total_chunks):
    """Processes a single CSV chunk through the entire bulk update flow."""
    print(f"\n--- Processing Chunk {chunk_num}/{total_chunks}: {csv_path} ---")
    jsonl_file_path = "temp_bulk_update.jsonl"

    if not generate_jsonl_from_csv(csv_path, jsonl_file_path):
        print(f"Failed to generate JSONL for {csv_path}. Skipping chunk.")
        return False
    
    graphql_client = setup_shopify_session()
    if not graphql_client:
        return False

    success = False
    try:
        staged_target = create_staged_upload(graphql_client, jsonl_file_path)
        if not staged_target: return False

        staged_upload_path = upload_file_to_staged_url(staged_target, jsonl_file_path)
        if not staged_upload_path: return False
            
        operation = run_bulk_mutation(graphql_client, staged_upload_path)
        if not operation or not operation.get('id'):
            print("Failed to start bulk mutation or get an operation ID.")
            return False

        # Before polling, wait to ensure the operation has started.
        print("Waiting 15 seconds before first poll...")
        time.sleep(15)

        completed_operation = poll_bulk_operation_status(graphql_client, operation['id'])
        if not completed_operation:
            print("Failed to get bulk operation completion status.")
            return False

        if completed_operation['status'] != 'COMPLETED':
             print("Bulk operation did not complete successfully.")
             print(f"Final status: {completed_operation['status']}, Error code: {completed_operation['errorCode']}")
             if completed_operation.get('url'):
                 print(f"A result file may still be available at: {completed_operation['url']}")
             return False

        download_and_process_results(completed_operation.get('url'))
        success = True

    finally:
        if os.path.exists(jsonl_file_path):
            os.remove(jsonl_file_path)
        
        shopify.ShopifyResource.clear_session()
        print(f"--- Finished Chunk {chunk_num}/{total_chunks} ---")
    
    return success

def main():
    parser = argparse.ArgumentParser(
        description="Bulk update Shopify variant prices using a CSV file.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
Example usage:
  python3 bulk_update_variants.py your_prices.csv

The CSV file must have a header row with 'variant_gid' and 'price' columns.
The script will automatically split large CSVs into smaller chunks.
"""
    )
    parser.add_argument("csv_file", help="Path to the CSV file containing variant GIDs and new prices.")
    args = parser.parse_args()

    temp_chunk_dir = "temp_variant_chunks"
    if not os.path.exists(args.csv_file):
        print(f"Error: Input file not found at '{args.csv_file}'")
        return

    # Create a temporary directory for the chunk files
    if os.path.exists(temp_chunk_dir):
        shutil.rmtree(temp_chunk_dir) # Clean up old directory if it exists
    os.makedirs(temp_chunk_dir)
    print(f"Created temporary directory for chunks: {temp_chunk_dir}")

    try:
        # Step 1: Split the large CSV into manageable chunks
        chunk_files = split_csv(args.csv_file, temp_chunk_dir, CHUNK_SIZE)
        total_chunks = len(chunk_files)
        
        if not chunk_files:
            print("No chunk files were created. Aborting.")
            return

        # Step 2: Process each chunk file sequentially
        successful_chunks = 0
        for i, chunk_path in enumerate(chunk_files):
            # Add a delay between chunks to avoid overwhelming the API
            if i > 0:
                print("\nWaiting for 10 seconds before starting next chunk...")
                time.sleep(10)

            if process_chunk(chunk_path, i + 1, total_chunks):
                successful_chunks += 1

        print(f"\n\n--- Overall Summary ---")
        print(f"Processed {total_chunks} chunk(s) in total.")
        print(f"Successful chunks: {successful_chunks}")
        print(f"Failed chunks: {total_chunks - successful_chunks}")
        print("-----------------------\n")

    finally:
        # Final cleanup of the temporary directory
        if os.path.exists(temp_chunk_dir):
            shutil.rmtree(temp_chunk_dir)
            print(f"Cleaned up temporary chunk directory: {temp_chunk_dir}")


if __name__ == "__main__":
    main() 