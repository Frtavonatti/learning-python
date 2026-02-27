# Learning Log

A simple Django web application built as a learning exercise following the **Python Crash Course** book by Eric Matthes (Chapter 18–20).

The app lets users register, log in, and keep track of topics they're learning about, with the ability to add and edit journal-style entries for each topic.

---

## Purpose

This project was built to learn the basics of Django, including:

- Setting up a Django project and apps
- Defining models and running migrations
- Using Django's built-in authentication system
- Writing views, URL patterns, and templates
- Restricting data access per user
- Styling with Bootstrap 3 via `django-bootstrap3`

---

## Project Structure

```
django/
├── manage.py
├── db.sqlite3
├── requirements.txt
│
├── learning_log/          # Project configuration
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── learning_logs/         # Main app: topics and entries
│   ├── models.py          # Topic and Entry models
│   ├── views.py           # View functions
│   ├── urls.py            # URL patterns for this app
│   ├── forms.py           # ModelForms for Topic and Entry
│   ├── admin.py           # Admin site registration
│   ├── migrations/        # Database migrations
│   └── templates/
│       └── learning_logs/
│           ├── base.html       # Base template with navbar
│           ├── index.html      # Home page
│           ├── topics.html     # List of topics
│           ├── topic.html      # Single topic with entries
│           ├── new_topic.html  # Form to create a topic
│           ├── new_entry.html  # Form to add an entry
│           └── edit_entry.html # Form to edit an entry
│
└── users/                 # Authentication app
    ├── views.py           # Register and logout views
    ├── urls.py            # URL patterns for auth
    ├── migrations/
    └── templates/
        └── users/
            ├── login.html     # Login page
            └── register.html  # Registration page
```

---

## Models

- **Topic** — a subject a user is tracking (e.g. "Chess", "Python"). Belongs to a single user.
- **Entry** — a dated journal entry associated with a topic.

---

## Running the Project

```bash
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Start the development server
python manage.py runserver
```

Then visit `http://localhost:8000`.
