# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
import os
import sqlite3

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
app.config['DATABASE'] = 'items.db'
app.secret_key = 'your_secret_key'  # Required for flashing messages

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def get_db():
    db = sqlite3.connect(app.config['DATABASE'])
    db.row_factory = sqlite3.Row
    return db

def init_db():
    with app.app_context():
        db = get_db()
        db.execute('''CREATE TABLE IF NOT EXISTS items
                      (id INTEGER PRIMARY KEY,
                       description TEXT,
                       brand TEXT,
                       model TEXT,
                       image TEXT)''')
        db.commit()

init_db()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    db = get_db()
    items = db.execute('SELECT * FROM items ORDER BY id').fetchall()
    return render_template('index.html', items=items)

@app.route('/add', methods=['GET', 'POST'])
def add_item():
    db = get_db()
    suggested_id = db.execute('SELECT MAX(id) FROM items').fetchone()[0]
    suggested_id = suggested_id + 1 if suggested_id else 1

    if request.method == 'POST':
        item_id = request.form['item_id']
        description = request.form['description']
        brand = request.form['brand']
        model = request.form['model']
        image = request.files['image']
        
        # Check if ID already exists
        existing_item = db.execute('SELECT id FROM items WHERE id = ?', (item_id,)).fetchone()
        if existing_item:
            flash('Item ID already exists. Please choose a different ID.', 'error')
            return render_template('add.html', suggested_id=item_id)
        
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{item_id}_{filename}")
            image.save(image_path)
            image_url = url_for('uploaded_file', filename=f"{item_id}_{filename}")
        else:
            image_url = None
        
        db.execute('INSERT INTO items (id, description, brand, model, image) VALUES (?, ?, ?, ?, ?)',
                   (item_id, description, brand, model, image_url))
        db.commit()
        
        flash('Item added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('add.html', suggested_id=suggested_id)

@app.route('/edit/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    db = get_db()
    item = db.execute('SELECT * FROM items WHERE id = ?', (item_id,)).fetchone()
    
    if not item:
        flash('Item not found', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        new_id = int(request.form['item_id'])
        description = request.form['description']
        brand = request.form['brand']
        model = request.form['model']
        image = request.files['image']
        
        # Check if new ID already exists (if changed)
        if new_id != item_id:
            existing_item = db.execute('SELECT id FROM items WHERE id = ?', (new_id,)).fetchone()
            if existing_item:
                flash('Item ID already exists. Please choose a different ID.', 'error')
                return render_template('edit.html', item=item)
        
        if image and image.filename != '' and allowed_file(image.filename):
            if item['image']:
                old_filename = os.path.basename(item['image'])
                try:
                    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], old_filename))
                except OSError:
                    app.logger.error(f"Error deleting old image: {old_filename}")
            
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{new_id}_{filename}")
            image.save(image_path)
            image_url = url_for('uploaded_file', filename=f"{new_id}_{filename}")
        else:
            image_url = item['image']
        
        if new_id != item_id:
            db.execute('DELETE FROM items WHERE id = ?', (item_id,))
        db.execute('INSERT OR REPLACE INTO items (id, description, brand, model, image) VALUES (?, ?, ?, ?, ?)',
                   (new_id, description, brand, model, image_url))
        db.commit()
        
        flash('Item updated successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('edit.html', item=item)

@app.route('/delete/<int:item_id>')
def delete_item(item_id):
    db = get_db()
    item = db.execute('SELECT * FROM items WHERE id = ?', (item_id,)).fetchone()
    
    if item:
        if item['image']:
            filename = os.path.basename(item['image'])
            try:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            except OSError:
                app.logger.error(f"Error deleting image: {filename}")
        
        db.execute('DELETE FROM items WHERE id = ?', (item_id,))
        db.commit()
        flash('Item deleted successfully!', 'success')
    else:
        flash('Item not found', 'error')
    return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
else:
    init_db()
