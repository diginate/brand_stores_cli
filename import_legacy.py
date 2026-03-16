import csv
import sys
import db
import datetime

def import_csv(filename):
    try:
        with open(filename, 'r', encoding='utf-8-sig') as csvfile: # Handle BOM if present
            reader = csv.DictReader(csvfile)
            
            skipped_na = 0
            stores_to_add = []
            
            # Normalize headers to handle potential whitespace or case issues
            # We'll just access by the known names from the file
            
            for row in reader:
                # specific mapping for "CS CUSTOMERS - Sheet13.csv"
                customer_id = row.get('ID') or row.get('customer_id')
                first_name = row.get('First Name') or row.get('first_name')
                last_name = row.get('Last Name') or row.get('last_name')
                email = row.get('Email') or row.get('email')
                url = row.get('Brand store') or row.get('url') or row.get('store_url')
                band_name = row.get('BAND NAME') or row.get('band_name') or row.get('artist_name')
                store_live = row.get('STORE LIVE')
                
                # Check if store is live
                if store_live and store_live.strip().upper() != 'YES':
                    # If STORE LIVE column exists and is not YES, skip
                    skipped_na += 1
                    continue

                if not customer_id:
                    print(f"Skipping row with missing customer_id: {row}")
                    continue

                # Use current date for legacy imports if no date provided
                date_live = row.get('date_live') or row.get('date')
                if not date_live:
                    date_live = datetime.date.today().strftime('%Y-%m-%d')

                stores_to_add.append({
                    'customer_id': customer_id,
                    'url': url,
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name,
                    'band_name': band_name,
                    'date_live': date_live
                })
            
            print(f"Found {len(stores_to_add)} stores to process.")
            print(f"Skipped {skipped_na} stores (Not Live/NA).")
            
            if stores_to_add:
                added_count = db.add_stores_bulk(stores_to_add)
                print(f"Import completed.")
                print(f"  Added: {added_count}")
                print(f"  Skipped (Already Exists): {len(stores_to_add) - added_count}")
            else:
                print("No stores to add.")

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
