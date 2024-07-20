# Flask Item Management System

## Overview

This Flask-based web application provides a simple and intuitive interface for managing items with descriptions, tags, and associated images. It allows users to create, read, update, and delete items, as well as add and remove tags and images for each item.

## Features

- Create new items with descriptions, tags, and images
- View a list of all items
- Edit existing items (update description, add/remove tags, add/remove images)
- Delete items
- Automatic ID assignment with option for manual entry
- Image upload and management
- Tag management for easy item categorization

## Technologies Used

- Python 3.8+
- Flask 2.1.0
- SQLAlchemy (via Flask-SQLAlchemy)
- HTML/CSS
- JavaScript (for frontend interactivity)

## Setup and Installation

1. Clone the repository:
   ```
   git clone https://github.com/bordessoules/webapp.git
   cd webapp
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the root directory and add the following:
   ```
   FLASK_APP=run.py
   FLASK_ENV=development
   SECRET_KEY=your_secret_key_here
   ```

5. Initialize the database:
   ```
   flask db upgrade
   ```

6. Run the application:
   ```
   flask run
   ```
7. Open a web browser and navigate to `http://localhost:5000`

## With docker
   ```
   docker-compose up --build
   ```
Open a web browser and navigate to `http://localhost:5000`

## Usage

### Adding an Item
1. Click on "Add New Item" from the homepage.
2. Fill in the description, add tags (comma-separated), and upload images.
3. Optionally, you can specify a custom ID or let the system auto-assign one.
4. Click "Add Item" to save.

### Editing an Item
1. From the item list, click on "Edit" next to the item you want to modify.
2. Update the description, add/remove tags, or add/remove images as needed.
3. Click "Update Item" to save changes.

### Deleting an Item
1. From the item list, click on "Delete" next to the item you want to remove.
2. Confirm the deletion when prompted.

## File Structure

```
flask-item-management/
│
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── helpers.py
│   └── templates/
│       ├── base.html
│       ├── index.html
│       ├── add.html
│       └── edit.html
│
├── .env
├── .gitignore
├── requirements.txt
├── app.py
└── README.md
```

## Contributing

Contributions are welcome! Please follow these steps to contribute:
    Fork the repository
    Create a new branch (git checkout -b feature-branch)
    Commit your changes (git commit -am 'Add new feature')
    Push to the branch (git push origin feature-branch)
    Create a new Pull Request

## License

This project is licensed under Apache License - see the LICENSE file for details or at 'https://www.apache.org/licenses/LICENSE-2.0'.
