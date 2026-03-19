# Flask Web Application

A simple Flask web application with user authentication, dashboard, and CRUD operations.

## Features

- User registration and login
- User management (CRUD operations)
- Dashboard with user listing
- Password hashing with bcrypt
- SQLite database integration

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Access the application at `http://localhost:5000`

## Directory Structure

```
flask_app/
├── app.py              # Main application file
├── requirements.txt    # Dependencies
├── templates/
│   ├── base.html       # Base template
│   ├── login.html      # Login page
│   ├── register.html   # Registration page
│   ├── dashboard.html  # Dashboard page
│   ├── add_user.html   # Add user page
│   └── edit_user.html  # Edit user page
└── static/
    └── style.css       # Optional CSS styling
```