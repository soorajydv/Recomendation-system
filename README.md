# Mindmorph Course Recommendation Server

The **Mindmorph Course Recommendation Server** is a service designed to recommend relevant courses to users of the Mindmorph e-learning platform. Built using **Django**, this server integrates with the platform to provide personalized course recommendations based on user preferences, previous activities, and other relevant data.

## Features

- Personalized course recommendations based on user behavior.
- Integration with the Mindmorph platform to fetch user data.
- Scalable and easy-to-maintain architecture built with Django.
- Easy configuration for developers and administrators.

## Requirements

- Python 3.8 or higher
- Django 4.0 or higher
- PostgreSQL (or another relational database)
- Redis (for caching)
- Celery (for asynchronous tasks)

## Installation

### Step 1: Clone the repository
```bash
git clone https://github.com/soorajydv/Recomendation-system.git
cd Recomendation-system
```
### Step 2: Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```
### Step 3: Run project
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
