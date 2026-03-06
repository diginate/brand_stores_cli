#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Check if arguments were provided
if [ $# -lt 2 ]; then
    echo "Error: Missing arguments"
    echo "Usage: $0 <product_id> <path_to_images_directory>"
    exit 1
fi

PRODUCT_ID="$1"
IMAGE_DIR="$2"

# Load environment variables from .env file if it exists
if [ -f "$SCRIPT_DIR/.env" ]; then
    export $(grep -v '^#' "$SCRIPT_DIR/.env" | xargs)
fi

echo "Running image upload for Product ID: $PRODUCT_ID"
echo "From directory: $IMAGE_DIR"
echo "Using Bucket: $S3_BUCKET_NAME ($AWS_DEFAULT_REGION)"
echo "------------------------------------"

python3 "$SCRIPT_DIR/upload_images.py" "$PRODUCT_ID" "$IMAGE_DIR"

if [ $? -eq 0 ]; then
    echo "------------------------------------"
    echo "Upload completed successfully!"
else
    echo "------------------------------------"
    echo "Upload failed. Please check your AWS credentials and try again."
fi
