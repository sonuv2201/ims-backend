## step 1
### pip install -r requirements.txt

## step 2:
### nish\nish_django_lcnc_backend\nish\settings.py

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "nish",
        "USER": "postgres",
        "PASSWORD": "admin",
        "HOST": "127.0.0.1",
        "PORT": "5432",  # Default PostgreSQL port
    }
}

## step 3:

python manage.py runserver
