# Shopify CLI App

A command-line interface to administer your Shopify store.

## Setup

1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Configure Shopify API credentials (details to be added).

## Usage

`./app.py [command] [options]`

## Bulk Updating Variant Prices

This tool allows you to update the prices of thousands of product variants at once using a CSV file. This is a two-step process.

### Step 1: Generate a list of all your product variants

First, you need to create a master CSV file that contains all the product variants you want to update.

1.  **Create a simple text file** named `handles.txt` in the `shopify_cli_app` directory.

2.  **Add your product handles** to this file, with one handle per line. A product handle is the last part of the URL when you view a product in your Shopify admin (e.g., `custom-hoodie-6043510538394`). Your `handles.txt` file should look like this:
    ```
    custom-hoodie-6043510538394
    die-cut-vinyl-stickers-5883839955098
    custom-tee-black-5900233408666
    ```

3.  **Run the script** from your terminal to generate the CSV file. You can optionally pre-fill a price for all variants at this stage.

    *   To generate the CSV with a blank 'price' column (for manual entry):
        ```bash
        python3 generate_variant_csv.py handles.txt variants.csv
        ```
    *   To generate the CSV and set a price of `24.99` for ALL variants:
        ```bash
        python3 generate_variant_csv.py handles.txt variants.csv --price 24.99
        ```

4.  This will create a new file named `variants.csv`. It will contain the unique `variant_gid` for every variant of every product you listed, along with other details like the SKU and current price.

### Step 2: Update the prices in Shopify

Now that you have your `variants.csv` file, you can update the prices.

1.  **Edit the `variants.csv` file** in any spreadsheet program (like Excel, Google Sheets, or Numbers). Fill in the `price` column with your new prices. Make sure you save your changes.

2.  **Run the bulk update script** from your terminal:
    ```bash
    python3 bulk_update_variants.py variants.csv
    ```

3.  The script will now begin the update process. It will automatically break your file into smaller chunks and process them one by one. You will see progress updates in the terminal. **This process can take a long time if you have many variants, so let it run until it is completely finished.**

Once it's done, it will show a summary of how many variants were updated. 