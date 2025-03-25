# TMC Website

This is the TMC website built using Django and Wagtail. This project serves as a template for creating a content management system (CMS) using Wagtail.

## Project Structure

```
tmc-website
├── config
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── home
│   ├── __init__.py
│   ├── models.py
│   ├── templates
│   │   └── home
│   │       └── index.html
│   ├── static
│   │   └── home
│   │       └── style.css
│   └── migrations
│       └── __init__.py
├── manage.py
├── requirements.txt
└── README.md
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd tmc-website
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the requirements:**
   ```
   pip install -r requirements.txt
   ```

4. **Run migrations:**
   ```
   python manage.py migrate
   ```

5. **Create a superuser:**
   ```
   python manage.py createsuperuser
   ```

6. **Run the development server:**
   ```
   python manage.py runserver
   ```

7. **Run makemigrations:**
   ```
   python manage.py makemigrations
   ```

8. **Run migrate:**
   ```
   python manage.py migrate
   ```

## Usage

- Access the admin panel at `http://127.0.0.1:8000/admin/` to manage your content.
- The home page can be accessed at `http://127.0.0.1:8000/`.

## License

This project is licensed under the MIT License.