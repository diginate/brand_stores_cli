import sys
import db

def check_store(customer_id):
    store = db.get_store(customer_id)
    if store:
        print(f"Store with ID {customer_id} already exists.")
        sys.exit(0) # Exit with 0 if store exists
    else:
        print(f"Store with ID {customer_id} does not exist.")
        sys.exit(1) # Exit with 1 if store does not exist

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python check_store.py <customer_id>")
        sys.exit(2)
    
    customer_id = sys.argv[1]
    check_store(customer_id)
