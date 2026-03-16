import json
import datetime
import os
import subprocess
import sqlite3

DB_FILE = 'stores.json'
SQLITE_DB = 'stores.db'

def run_git_command(command):
    try:
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Git command failed: {' '.join(command)}")
        print(e.stderr.decode())
        return False

def sync_pull():
    print("Syncing with remote (pull)...")
    return run_git_command(['git', 'pull', '--rebase'])

def sync_push(message="Update stores database"):
    print("Syncing with remote (push)...")
    if run_git_command(['git', 'add', DB_FILE]):
        if run_git_command(['git', 'commit', '-m', message]):
            return run_git_command(['git', 'push'])
    return False

def load_data():
    if not os.path.exists(DB_FILE):
        return []
    try:
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_data(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def migrate_from_sqlite():
    if os.path.exists(SQLITE_DB) and not os.path.exists(DB_FILE):
        print("Migrating from SQLite to JSON...")
        try:
            conn = sqlite3.connect(SQLITE_DB)
            conn.row_factory = sqlite3.Row
            rows = conn.execute('SELECT * FROM stores').fetchall()
            data = []
            for row in rows:
                data.append({
                    'customer_id': row['customer_id'],
                    'url': row['url'],
                    'email': row['email'],
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'band_name': row['band_name'],
                    'date_live': row['date_live']
                })
            conn.close()
            save_data(data)
            print(f"Migrated {len(data)} records.")
            # Optional: rename old db to avoid confusion
            os.rename(SQLITE_DB, SQLITE_DB + '.bak')
        except Exception as e:
            print(f"Migration failed: {e}")

def init_db():
    # Check for migration
    migrate_from_sqlite()
    
    if not os.path.exists(DB_FILE):
        save_data([])
        
    # Try to pull latest changes on init
    sync_pull()

def add_store(customer_id, url, email, first_name, last_name, band_name, date_live=None):
    # Pull latest before adding to avoid conflicts
    sync_pull()
    
    data = load_data()
    
    # Check for duplicates
    for store in data:
        if store['customer_id'] == customer_id:
            return False
            
    if date_live is None:
        date_live = datetime.date.today().strftime('%Y-%m-%d')
    
    new_store = {
        'customer_id': customer_id,
        'url': url,
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'band_name': band_name,
        'date_live': date_live
    }
    
    data.append(new_store)
    save_data(data)
    
    # Push changes
    sync_push(f"Add store {customer_id}")
    
    return True

def add_stores_bulk(stores_list):
    """
    Add multiple stores at once.
    stores_list: list of dicts with keys: customer_id, url, email, first_name, last_name, band_name, date_live
    """
    # Pull latest before adding
    sync_pull()
    
    data = load_data()
    existing_ids = {store['customer_id'] for store in data}
    
    added_count = 0
    for store in stores_list:
        if store['customer_id'] in existing_ids:
            continue
            
        if not store.get('date_live'):
            store['date_live'] = datetime.date.today().strftime('%Y-%m-%d')
            
        data.append(store)
        existing_ids.add(store['customer_id'])
        added_count += 1
    
    if added_count > 0:
        save_data(data)
        sync_push(f"Bulk add {added_count} stores")
        return added_count
    else:
        return 0

def get_store(customer_id):
    # We don't pull here to keep reads fast, relying on init_db or manual sync
    # But for critical checks, maybe we should? 
    # Let's assume the user runs init_db or the script calls sync_pull if needed.
    data = load_data()
    for store in data:
        if store['customer_id'] == customer_id:
            return store
    return None

def get_all_stores():
    data = load_data()
    # Sort by date_live desc
    try:
        return sorted(data, key=lambda x: x.get('date_live', ''), reverse=True)
    except:
        return data

if __name__ == '__main__':
    init_db()
    print("Database initialized (JSON + Git).")
