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

# Define miscellaneous item types
MISC_ITEM_TYPES=(
  "custom-white-mug"
  "custom-bottle-opener"
)

# Create all miscellaneous item products
echo "Creating all miscellaneous item products with ID $PRODUCT_ID..."
for item_type in "${MISC_ITEM_TYPES[@]}"; do
  echo "------------------------------------"
  echo "Creating $item_type product..."
  python3 "$SCRIPT_DIR/app.py" create-product --template-key $item_type --id $PRODUCT_ID
  echo "$item_type product creation completed."
  echo "------------------------------------"
  # Small delay between requests to avoid rate limiting
  sleep 5
done

echo "All miscellaneous item products created successfully!" 