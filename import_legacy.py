import csv
import sys
import db
import datetime

def import_csv(filename):
    try:
        with open(filename, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0
            for row in reader:
                # Map CSV columns to DB columns if necessary
                # Assuming CSV headers match DB columns or are close enough
                customer_id = row.get('customer_id') or row.get('id')
                url = row.get('url') or row.get('store_url')
                email = row.get('email')
                first_name = row.get('first_name')
                last_name = row.get('last_name')
                band_name = row.get('band_name') or row.get('artist_name')
                date_live = row.get('date_live') or row.get('date')

                if not customer_id:
                    print(f"Skipping row with missing customer_id: {row}")
                    continue

                if db.add_store(customer_id, url, email, first_name, last_name, band_name, date_live):
                    print(f"Added store: {customer_id}")
                    count += 1
                else:
                    print(f"Store {customer_id} already exists or failed to add.")
            
            print(f"Import completed. Added {count} stores.")

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except Exception as e:
        print(f"Error importing CSV: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python import_legacy.py <csv_filename>")
        sys.exit(1)
    
    filename = sys.argv[1]
    db.init_db() # Ensure DB is initialized
    import_csv(filename)
