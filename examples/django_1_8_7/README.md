## How to run this demo

Assume you are in this directory (django_1_8_2)

    # Create the virtual environment
    virtualenv .env

    # Activate the environment
    source .env/bin/activate

    # Install dependencies
    pip install -r requirements.txt

    # Install drf redocs
    pip install -e ../../

    # Init django site
    python manage.py makemigrations
    python manage.py migrate
    python manage.py createsuperuser

    # Run the project
    python manage.py runserver


### Viewing Docs

Once you install and run the project go to [http://0.0.0.0:8000/docs/](http://0.0.0.0:8000/redocs/).


### Note
The demo project is mostly based on [django_rest_framework_docs](https://github.com/manosim/django-rest-framework-docs/), thanks for their great work!
