from flask import Flask, render_template, request, redirect, url_for, flash
import db
import os
from dotenv import load_dotenv
import upload_images
import shopify_customer
import tempfile
import shutil
import re

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = 'supersecretkey' # Needed for flash messages

@app.route('/')
def index():
    stores = db.get_all_stores()
    return render_template('index.html', stores=stores)

@app.route('/add', methods=['GET', 'POST'])
def add_store():
    if request.method == 'POST':
        customer_id = request.form['customer_id']
        url = request.form['url']
        email = request.form['email']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        band_name = request.form['band_name']
        
        if db.add_store(customer_id, url, email, first_name, last_name, band_name):
            flash(f'Store {customer_id} added successfully!', 'success')
        else:
            flash(f'Store {customer_id} already exists or failed to add.', 'error')
            
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/upload-new', methods=['POST'])
def upload_new_store():
    print("Received upload-new request")
    # Check if files were uploaded
    if 'files' not in request.files:
        print("No file part in request")
        flash('No file part', 'error')
        return redirect(url_for('index'))
        
    files = request.files.getlist('files')
    
    if not files or files[0].filename == '':
        print("No selected file")
        flash('No selected file', 'error')
        return redirect(url_for('index'))

    # Extract Product ID from the first file path
    # Assuming path is like "PRODUCT_ID/..." or "PRODUCT_ID/image.jpg"
    first_path = files[0].filename
    # Handle cases where filename might start with /
    if first_path.startswith('/'):
        first_path = first_path[1:]
        
    product_id = first_path.split('/')[0]
    print(f"Detected Product ID from upload: {product_id}")
    
    if not product_id:
        print("Could not determine Product ID")
        flash('Could not determine Product ID from folder name.', 'error')
        return redirect(url_for('index'))

    # Create a temporary directory to store uploaded files
    with tempfile.TemporaryDirectory() as temp_dir:
        file_count = 0
        for file in files:
            if file.filename:
                # Determine save path
                # We'll save relative to temp_dir
                # Remove leading slash if present
                clean_filename = file.filename
                if clean_filename.startswith('/'):
                    clean_filename = clean_filename[1:]
                    
                file_path = os.path.join(temp_dir, clean_filename)
                
                # Ensure directory exists
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                
                file.save(file_path)
                file_count += 1
        
        if file_count == 0:
            print("No valid files found in upload")
            flash('No valid files found in upload.', 'error')
            return redirect(url_for('index'))
            
        # Call the upload script
        # We pass the temp_dir as the source directory
        # The script will look for product_id folder or _previews folder inside, or use root
        print(f"Starting upload to S3 for {product_id}...")
        success, message, count = upload_images.upload_directory_to_s3(product_id, temp_dir)
        
        if success:
            print(f"Upload successful: {count} files")
            flash(f'Successfully uploaded {count} images for new store {product_id} to S3.', 'success')
            
            # Fetch customer details from Shopify
            try:
                print(f"Querying Shopify for customer {product_id}...")
                customer = shopify_customer.get_shopify_customer(product_id)
                if customer:
                    print(f"Customer found: {customer['first_name']} {customer['last_name']}")
                    # Construct URL
                    store_url = f"https://customskins.co.uk/collections/{product_id}"
                    
                    # Add to DB
                    print(f"Attempting to add store {product_id} to database...")
                    if db.add_store(
                        customer_id=product_id,
                        url=store_url,
                        email=customer['email'],
                        first_name=customer['first_name'],
                        last_name=customer['last_name'],
                        band_name="" # Band name not available in customer data
                    ):
                        print(f"Store {product_id} created successfully.")
                        flash(f'Store {product_id} created in database with details from Shopify.', 'success')
                    else:
                        print(f"Store {product_id} already exists in database.")
                        flash(f'Store {product_id} already exists in database.', 'info')
                else:
                    print(f"Customer {product_id} not found in Shopify.")
                    flash(f'Could not find customer {product_id} in Shopify. Store not created in DB.', 'warning')
            except Exception as e:
                print(f"Error fetching customer details: {str(e)}")
                flash(f'Error fetching customer details: {str(e)}', 'error')
                
        else:
            print(f"Upload failed: {message}")
            flash(f'Upload failed for {product_id}: {message}', 'error')
            
        return redirect(url_for('index'))

@app.route('/upload/<customer_id>', methods=['GET', 'POST'])
def upload_store_images(customer_id):
    store = db.get_store(customer_id)
    if not store:
        flash(f'Store {customer_id} not found.', 'error')
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        # Check if files were uploaded
        if 'files' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)
            
        files = request.files.getlist('files')
        
        if not files or files[0].filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)

        # Create a temporary directory to store uploaded files
        with tempfile.TemporaryDirectory() as temp_dir:
            file_count = 0
            for file in files:
                if file.filename:
                    # Determine save path
                    # We'll save relative to temp_dir
                    clean_filename = file.filename
                    if clean_filename.startswith('/'):
                        clean_filename = clean_filename[1:]
                    
                    file_path = os.path.join(temp_dir, clean_filename)
                    
                    # Ensure directory exists
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    
                    file.save(file_path)
                    file_count += 1
            
            if file_count == 0:
                flash('No valid files found in upload.', 'error')
                return redirect(request.url)
                
            # Call the upload script
            success, message, count = upload_images.upload_directory_to_s3(customer_id, temp_dir)
            
            if success:
                flash(f'Successfully uploaded {count} images to S3.', 'success')
                return redirect(url_for('index'))
            else:
                flash(f'Upload failed: {message}', 'error')
                return redirect(request.url)

    return render_template('upload.html', store=store)

@app.route('/sync')
def sync():
    if db.sync_pull():
        flash('Successfully synced with remote.', 'success')
    else:
        flash('Failed to sync with remote. Check console for details.', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.init_db()
    app.run(debug=True, port=5000)
