from flask import Flask, render_template, request, redirect, url_for, flash
import db

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
