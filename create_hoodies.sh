#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Check if ID was provided as an argument
if [ $# -eq 0 ]; then
    echo "Error: Please provide a product ID"
    echo "Usage: $0 <product_id>"
    exit 1
fi

# Get ID from command line argument
PRODUCT_ID="$1"

# Define the hoodie template key
HOODIE_TEMPLATE_KEY="custom-hoodie"

# Create the hoodie product
echo "Creating $HOODIE_TEMPLATE_KEY product with ID $PRODUCT_ID..."
echo "------------------------------------"
python3 "$SCRIPT_DIR/app.py" create-product --template-key $HOODIE_TEMPLATE_KEY --id $PRODUCT_ID
echo "------------------------------------"
echo "$HOODIE_TEMPLATE_KEY product creation completed."

echo "Hoodie product created successfully!" 