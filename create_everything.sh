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

# Check if store exists in DB
# check_store.py returns 0 if store exists, 1 if it doesn't
python3 "$SCRIPT_DIR/check_store.py" "$PRODUCT_ID"
STORE_EXISTS=$?

if [ $STORE_EXISTS -eq 0 ]; then
    echo "Store with ID $PRODUCT_ID already exists in the database. Skipping creation."
    exit 0
fi

echo "Store with ID $PRODUCT_ID does not exist. Creating new store..."
echo "Please enter the following details:"

read -p "Store URL: " STORE_URL
read -p "Customer Email: " CUSTOMER_EMAIL
read -p "First Name: " FIRST_NAME
read -p "Last Name: " LAST_NAME
read -p "Band/Artist Name: " BAND_NAME

# Add store to DB
python3 "$SCRIPT_DIR/add_store_cli.py" "$PRODUCT_ID" --url "$STORE_URL" --email "$CUSTOMER_EMAIL" --first-name "$FIRST_NAME" --last-name "$LAST_NAME" --band-name "$BAND_NAME"

if [ $? -ne 0 ]; then
    echo "Error: Failed to add store to database. Aborting."
    exit 1
fi

echo "Store added to database successfully."
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
