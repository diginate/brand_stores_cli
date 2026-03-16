import sys
import argparse
import db

def main():
    parser = argparse.ArgumentParser(description="Add a store to the database.")
    parser.add_argument("customer_id", help="Customer ID")
    parser.add_argument("--url", required=True, help="Store URL")
    parser.add_argument("--email", required=True, help="Customer Email")
    parser.add_argument("--first-name", required=True, help="Customer First Name")
    parser.add_argument("--last-name", required=True, help="Customer Last Name")
    parser.add_argument("--band-name", required=True, help="Band/Artist Name")
    
    args = parser.parse_args()
    
    success = db.add_store(args.customer_id, args.url, args.email, args.first_name, args.last_name, args.band_name)
    
    if success:
        print(f"Store {args.customer_id} added successfully.")
        sys.exit(0)
    else:
        print(f"Failed to add store {args.customer_id}. It might already exist.")
        sys.exit(1)

if __name__ == "__main__":
    main()
