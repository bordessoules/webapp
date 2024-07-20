# routes.py
from flask import Blueprint, render_template, request, redirect, flash, current_app, jsonify, send_from_directory
import os
from app import db
from app.models import Item, Image, Tag
from .helpers import generate_unique_filename, allowed_file
from sqlalchemy.exc import IntegrityError

main = Blueprint('main', __name__)
def get_next_id(items):
    last_item = items.query.order_by(Item.id.desc()).first()
    if last_item:
        return last_item.id + 1
    return 1
def save_image(image):
    if image and allowed_file(image.filename):
        filename = generate_unique_filename(image.filename)
        image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        image.save(image_path)
        return filename
    return None

@main.route('/')
def index():
    items = Item.query.all()
    return render_template('index.html', items=items)

@main.route('/uploads/<filename>')
def uploaded_file(filename):
    uploads_dir = current_app.config['UPLOAD_FOLDER']
    # Ensure the path is absolute
    uploads_dir = os.path.abspath(uploads_dir)
    current_app.logger.info(f"Attempting to serve file: {filename} from directory: {uploads_dir}")
    
    if os.path.exists(os.path.join(uploads_dir, filename)):
        current_app.logger.info(f"File {filename} found in {uploads_dir}")
    else:
        current_app.logger.error(f"File {filename} not found in {uploads_dir}")
    
    return send_from_directory(uploads_dir, filename)

@main.route('/add', methods=['GET', 'POST'])
def add_item():
   
    if request.method == 'POST':              
        description = request.form.get('description')
        tags = request.form.get('tags', '').split(',')
        # Handle optional ID
        item_id = request.form.get('id')
        if item_id:
            # Check if an item with this ID already exists
            existing_item = Item.query.get(item_id)
            if existing_item:
                return jsonify({'success': False, 'message': 'An item with this ID already exists.'}), 400
            new_item = Item(id=item_id, description=description)
        else:
            new_item = Item(description=description)

        # Handle tags
        for tag in tags:
            if tag:
                new_item.add_tag(tag.strip())

        # Handle images
        if 'images' in request.files:
            images = request.files.getlist('images')
            for image in images:
                if image and image.filename and allowed_file(image.filename):
                    filename = generate_unique_filename(image.filename)
                    image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                    image.save(image_path)
                    new_image = Image(filename=filename)
                    new_item.images.append(new_image)
                    current_app.logger.info(f"File saved and associated with item: {filename}")
                else:
                    current_app.logger.warning(f"Invalid file: {image.filename}")
        else:
            current_app.logger.warning("No 'images' in request.files")

        try:
            db.session.add(new_item)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Item added successfully!'}), 200
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error adding item to database: {str(e)}")
            return jsonify({'success': False, 'message': 'Error adding item'}), 500
    
    suggested_id = get_next_id(Item)
    return render_template('add.html', suggested_id=suggested_id)

@main.route('/edit/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    item = Item.query.get_or_404(item_id)

    if request.method == 'POST':
        item.description = request.form['description']

        # Handle tags
        new_tags = request.form['tags'].split(',')
        item.tags.clear()
        for tag_name in new_tags:
            tag_name = tag_name.strip()
            if tag_name:
                item.add_tag(tag_name)

        # Handle new images
        if 'new_images' in request.files:
            for image in request.files.getlist('new_images'):
                if image and allowed_file(image.filename):
                    filename = generate_unique_filename(image.filename)
                    image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                    image.save(image_path)
                    new_image = Image(filename=filename)
                    item.images.append(new_image)

        # Handle image removals
        if 'remove_images' in request.form:
            for filename in request.form.getlist('remove_images'):
                image = Image.query.filter_by(filename=filename).first()
                if image and image in item.images:
                    item.images.remove(image)
                    db.session.delete(image)
                    # Optionally, remove the file from the filesystem
                    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                    if os.path.exists(file_path):
                        os.remove(file_path)

        try:
            db.session.commit()
            return jsonify({'success': True, 'message': 'Item updated successfully!'}), 200
        except IntegrityError:
            db.session.rollback()
            return jsonify({'success': False, 'message': 'An error occurred. Please try again.'}), 500

    return render_template('edit.html', item=item)
@main.route('/delete/<int:item_id>')
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)

    # Delete associated images
    for image in item.images:
        os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], image.filename))

    db.session.delete(item)
    db.session.commit()

    flash('Item deleted successfully!', 'success')
    return redirect('/')
