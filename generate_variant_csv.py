#!/usr/bin/env python3
import shopify
import os
import argparse
import json
import time
import csv
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Shopify Credentials ---
API_KEY = os.getenv("SHOPIFY_API_KEY")
PASSWORD = os.getenv("SHOPIFY_PASSWORD")
SHOP_NAME = os.getenv("SHOPIFY_SHOP_NAME")
API_VERSION = os.getenv("SHOPIFY_API_VERSION", "2024-04")

# --- GraphQL Query ---
GET_VARIANTS_BY_HANDLE_QUERY = """
query productByHandle($handle: String!) {
  productByHandle(handle: $handle) {
    id
    handle
    title
    variants(first: 100) {
      edges {
        node {
          id
          title
          sku
          price
        }
      }
    }
  }
}
"""

def setup_shopify_session():
    """Initializes the Shopify API session and returns a GraphQL client."""
    try:
        shop_url = f"https://{API_KEY}:{PASSWORD}@{SHOP_NAME}.myshopify.com/admin"
        session = shopify.Session(shop_url, API_VERSION, PASSWORD)
        shopify.ShopifyResource.activate_session(session)
        print("Shopify session activated.")
        return shopify.GraphQL()
    except Exception as e:
        print(f"Error activating Shopify session: {e}")
        return None

def fetch_variants_for_handle(graphql_client, handle):
    """Fetches all variants for a given product handle."""
    try:
        variables = {"handle": handle}
        result_str = graphql_client.execute(GET_VARIANTS_BY_HANDLE_QUERY, variables=variables)
        result = json.loads(result_str)

        if "errors" in result:
            print(f"  - GraphQL Error for handle '{handle}': {result['errors']}")
            return None

        product_data = result.get("data", {}).get("productByHandle")
        if not product_data:
            print(f"  - Product with handle '{handle}' not found.")
            return [] # Return empty list for not found

        return product_data
        
    except Exception as e:
        print(f"  - An exception occurred fetching handle '{handle}': {e}")
        return None

def generate_variants_csv(handles_file_path, output_csv_path, new_price=''):
    """
    Reads a file of product handles, fetches their variants from Shopify,
    and writes the variant details to a CSV file.
    """
    graphql_client = setup_shopify_session()
    if not graphql_client:
        return

    print(f"Reading handles from: {handles_file_path}")
    try:
        with open(handles_file_path, 'r') as f:
            handles = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"ERROR: Input file with handles not found at '{handles_file_path}'")
        return

    print(f"Found {len(handles)} handles to process.")
    
    total_variants_found = 0
    try:
        with open(output_csv_path, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            # Write header
            writer.writerow(['variant_gid', 'product_handle', 'product_title', 'variant_title', 'sku', 'current_price', 'price'])
            
            for i, handle in enumerate(handles):
                print(f"Processing handle {i+1}/{len(handles)}: '{handle}'...")
                product_data = fetch_variants_for_handle(graphql_client, handle)
                
                if product_data:
                    variants = product_data.get('variants', {}).get('edges', [])
                    if not variants:
                        print(f"  - No variants found for handle '{handle}'.")
                    
                    for variant_edge in variants:
                        variant_node = variant_edge['node']
                        writer.writerow([
                            variant_node['id'],
                            product_data['handle'],
                            product_data['title'],
                            variant_node['title'],
                            variant_node.get('sku', ''),
                            variant_node['price'],
                            new_price  # Use the provided price, or empty string if not provided
                        ])
                        total_variants_found += 1
                
                # Add a small delay to be kind to the Shopify API
                time.sleep(0.5)

    except Exception as e:
        print(f"An error occurred while writing the CSV: {e}")
    finally:
        shopify.ShopifyResource.clear_session()
        print("Shopify session cleared.")

    print(f"\nProcessing complete.")
    print(f"Found a total of {total_variants_found} variants.")
    print(f"CSV file generated at: {output_csv_path}")
    print("Next step: Fill in the 'price' column in the CSV and use it with the 'bulk_update_variants.py' script.")


def main():
    parser = argparse.ArgumentParser(
        description="Generate a CSV of product variants from a list of product handles.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
Example usage:
  # Just generate the file with current prices and an empty 'price' column
  python3 generate_variant_csv.py your_handles.txt variants_to_update.csv

  # Generate the file and pre-fill a new price for all variants
  python3 generate_variant_csv.py your_handles.txt variants_to_update.csv --price 24.99

The input file ('your_handles.txt') should contain one product handle per line.
"""
    )
    parser.add_argument("handles_file", help="Path to the input .txt file containing product handles (one per line).")
    parser.add_argument("output_csv", help="Path for the output CSV file that will be generated.")
    parser.add_argument("--price", help="Optional: A new price to set for all variants in the 'price' column.", default='')
    args = parser.parse_args()

    generate_variants_csv(args.handles_file, args.output_csv, args.price)


if __name__ == "__main__":
    main() 