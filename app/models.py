# models.py
from .helpers import generate_unique_filename, allowed_file
from flask import current_app
from werkzeug.utils import secure_filename
from app import db
import os

item_tags = db.Table('item_tags',
    db.Column('item_id', db.Integer, db.ForeignKey('item.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.name'), primary_key=True)
)

item_images = db.Table('item_images',
    db.Column('item_id', db.Integer, db.ForeignKey('item.id'), primary_key=True),
    db.Column('image_id', db.Integer, db.ForeignKey('image.filename'), primary_key=True)
)

class Image(db.Model):
    filename = db.Column(db.String(50), primary_key=True)

class Tag(db.Model):
    name = db.Column(db.String(50), primary_key=True)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(200), nullable=False)
    images = db.relationship('Image', secondary=item_images, lazy='subquery',
                             backref=db.backref('items', lazy=True))
    tags = db.relationship('Tag', secondary=item_tags, lazy='subquery',
                           backref=db.backref('items', lazy=True))

    def add_tag(self, tag_name):
        tag = Tag.query.get(tag_name)
        if not tag:
            tag = Tag(name=tag_name)
        if tag not in self.tags:
            self.tags.append(tag)

    def add_image(self, image_file):
        if not image_file:
            return None
        
        filename = secure_filename(image_file.filename)
        if not allowed_file(filename):
            raise ValueError("File type not allowed")
        
        image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        image_file.save(image_path)
        
        image = Image.query.get(filename)
        if not image:
            image = Image(filename=filename)
            db.session.add(image)
        
        if image not in self.images:
            self.images.append(image)
        
        return image