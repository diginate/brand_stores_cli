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

# Define colors
COLORS=(
  "custom-tee-small-logo"
)

# Create all products
echo "Creating all small logo tee variants with ID $PRODUCT_ID..."
for color in "${COLORS[@]}"; do
  echo "------------------------------------"
  echo "Creating $color product..."
  python3 "$SCRIPT_DIR/app.py" create-product --template-key $color --id $PRODUCT_ID
  echo "$color product creation completed."
  echo "------------------------------------"
  # Small delay between requests to avoid rate limiting
  sleep 3
done

echo "All small logo tees created successfully!"
