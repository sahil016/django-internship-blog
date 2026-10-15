# DevBlog — Django Internship Blog

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Django](https://img.shields.io/badge/Django-backend-092E20)
![Status](https://img.shields.io/badge/status-live-brightgreen)

A full-stack blog platform built with Django, featuring user authentication and post publishing. Built as a hands-on project during internship training.

**🚀 [Live Demo](https://devblog-app-vhtq.onrender.com)** — try it out, no setup required

## Features

- 📝 Create and publish blog posts
- 🔐 User registration and login
- 📰 Public feed of published articles
- 🎨 Clean, minimal UI

## Tech Stack

- **Python** 3.x
- **Django** (backend framework)
- **SQLite** (default database)
- **Render** (deployment)

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

- Uses SQLite by default — no separate database setup needed for local development
- The [live demo](https://devblog-app-vhtq.onrender.com) is deployed on Render and may take a few seconds to spin up on first load (free-tier cold start)
- For production, consider switching to PostgreSQL or MySQL

---

⭐ If you found this project useful, consider giving it a star!
