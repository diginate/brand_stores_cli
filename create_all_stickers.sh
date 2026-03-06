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

# Define sticker types
STICKER_TYPES=(
  "die-cut-vinyl-stickers"
  "die-cut-holographic-stickers"
  "die-cut-silver-stickers"
  "die-cut-gold-stickers"
  "die-cut-glitter-stickers"
)

# Create all sticker products
echo "Creating all sticker products with ID $PRODUCT_ID..."
for sticker_type in "${STICKER_TYPES[@]}"; do
  echo "------------------------------------"
  echo "Creating $sticker_type product..."
  python3 "$SCRIPT_DIR/app.py" create-product --template-key $sticker_type --id $PRODUCT_ID
  echo "$sticker_type product creation completed."
  echo "------------------------------------"
  # Small delay between requests to avoid rate limiting
  sleep 5
done

echo "All sticker products created successfully!" 