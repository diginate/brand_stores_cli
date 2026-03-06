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

echo "Starting full product creation process for ID: $PRODUCT_ID"
echo "========================================================"

# Function to run a script and check its exit code
run_script() {
    local script_name="$1"
    echo "Running $script_name..."
    "$SCRIPT_DIR/$script_name" "$PRODUCT_ID"
    
    if [ $? -ne 0 ]; then
        echo "Error: $script_name failed. Stopping process."
        exit 1
    fi
    echo "$script_name completed successfully."
    echo "--------------------------------------------------------"
    # Small delay between scripts
    sleep 2
}

# Run each creation script
run_script "create_all_colors.sh"
run_script "create_all_stickers.sh"
run_script "create_hoodies.sh"
run_script "create_misc_items.sh"

echo "All products created successfully!"
