# Rewarder Voucher System

## Overview
A robust API service designed for efficient voucher management and distribution. This system enables automated voucher creation and management for customer rewards programs.

## Key Features
- Automated voucher generation from CSV customer data
- Secure voucher creation for individual customers
- Comprehensive voucher retrieval and management
- RESTful API endpoints for seamless integration

## Technical Stack

### Core Technologies
- Python 3.x
- Django Framework
- Django Ninja

### Requirements
- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

## Getting Started

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/kowalski21/rewarder-app.git
   cd rewarder-app
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Configuration

1. Apply database migrations:
   ```bash
   python manage.py migrate
   ```

2. Create a superuser (optional):
   ```bash
   python manage.py createsuperuser
   ```

### Running the Server

1. Start the development server:
   ```bash
   python manage.py runserver
   ```

   ```bash
   ./start-celery.sh # to sta
```
2. Access the API at: `http://localhost:8000`

## API Documentation

The API documentation is available at: `http://localhost:8000/api/docs`

## Contributing

Please read our [Contributing Guidelines](CONTRIBUTING.md) before submitting pull requests.
## Support

For support and questions, please [open an issue](https://github.com/kowalski21/rewarder-app/issues) on our GitHub repository.


