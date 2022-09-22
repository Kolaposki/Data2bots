# Data2bots-API

An API for Data2bots Django Backend Developer Assessment

## Getting Started

Create a virtual environment to install dependencies and activate it:

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the required dependencies in requirements.txt.

```bash
(env)$ pip install -r requirements.txt
``` 

Then simply apply the migrations:

    $ python manage.py migrate

Create Superuser:

    $ python manage.py createsuperuser

You can now run the development server. Let's assume at port 9900 

    $ python manage.py runserver 9900 

## Docs
Swagger `http://127.0.0.1:9900/api/docs/`
