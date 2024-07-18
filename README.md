# WebApp

A simple Flask web application for managing products, including features for adding, editing, listing, and deleting products with QR codes and images.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Docker Usage](#docker-usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Introduction

This web application is built using Flask and provides a simple interface to manage products. Users can add new products with QR codes, edit existing ones, list all products, and delete products. The application uses SQLite for data storage and supports image uploads.

## Features

- Add new products with details and images
- Edit existing products
- List all products
- Delete products
- Image upload functionality

## Prerequisites

- Python 3.9+
- Docker (optional, for containerized deployment)

## Installation

1. **Clone the repository:**

    ```bash
    git clone[ https://github.com/bordessoules/webapp]
    cd webapp
    ```

2. **Create a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Run the application:**

    ```bash
    python app.py
    ```

## Usage

Once the application is running, you can access it at `http://localhost:5000`. You will see the following routes available:

- `/` - Home page
- `/api/list` - List all products
- `/api/add` - Add a new product
- `/api/edit<int:id>` - Edit a product
- `/api/delete-<int:qr_code>` - Delete a product

## Docker Usage

To run the application using Docker:

1. **Build and run the Docker container:**

    ```bash
    docker-compose up --build
    ```

2. Access the application at `http://localhost:5000`.

## Project Structure

```plaintext
/your-project-directory
├── app.py               # Main application file
├── Dockerfile           # Docker configuration
├── requirements.txt     # Python dependencies
├── docker-compose.yml   # Docker Compose configuration
├── uploads/             # Directory for uploaded images
└── templates/           # HTML templates for Flask
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
