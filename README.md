# Django Internship Blog

A simple blog application built with Django to manage and display blog posts.

## What It Does

This is a Django-based blog platform that allows you to create, read, and manage blog posts. It features a clean architecture with separate apps for blog functionality and core settings.

## Tech Stack

- **Python** 3.x
- **Django** (backend framework)
- **SQLite** (default database)

## Getting Started

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/sahil016/django-internship-blog.git
   cd django-internship-blog
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Start the development server**
   ```bash
   python manage.py runserver
   ```

   The application will be available at `http://localhost:8000/`

## Project Structure

```
django-internship-blog/
├── blog/              # Blog app (models, views, templates)
├── core/              # Core app (settings, configuration)
├── manage.py          # Django management script
└── requirements.txt   # Python dependencies
```

## Notes

- This project uses SQLite by default (no separate database setup needed)
- For production deployment, consider using PostgreSQL or MySQL

---

Built as a learning project during internship training.
