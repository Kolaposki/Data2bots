# Data2bots-API

An API for Data2bots Django Backend Developer Assessment

## Getting Started

Create a virtual environment to install dependencies and activate it:

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the required dependencies in requirements.txt.

```bash
(env)$ pip install -r requirements.txt
``` 

Generate a SECRET_KEY and add to SECRET_KEY variable in settings.py

    from django.core.management.utils import get_random_secret_key  

Then simply apply the migrations:

    $ python manage.py migrate

Create Superuser:

    $ python manage.py createsuperuser

You can now run the development server. Let's assume at port 9900 

    $ python manage.py runserver 9900 


## API
The REST API endpoints to the app is described below.

### Register
Create user. The data required are username, email, name, password and mobile (optional).

    URL : http://127.0.0.1:9900/api/user/register/

    Method : POST


### Login
Login a user. Takes a set of username and password and returns an access and refresh JSON web
token pair to prove the authentication of those credentials. Use this access token in the Authorization header as Bearer to authenticate.

    URL : http://127.0.0.1:9900/api/token/

    Method : POST

    Body :    {
                username: 'admin',
                password: '1234'
              }

### Profile
Returns a profile, provided the authorization token in header.

    URL : http://127.0.0.1:9900/api/user/account/

    Method : GET


### Update Profile
Update the profile of a user, provided the authorization token in header.

    URL : http://127.0.0.1:9900/api/user/account/

    Method : PATCH

    Body :    {
                username: 'admin',
                password: '1234'
                email: 'admin@example.com',
                name: 'John Doe',
              }

### Products
Returns all products in database. Create products initially using the admin dashboard.

    URL : http://127.0.0.1:9900/api/product/

    Method : GET


### Payment
Make payment to an account provided the authorization token in header. Method of payment must be in CAPS (CASH or CARD)

    URL : http://127.0.0.1:9900/api/user/account/

    Method : POST

    Body :    {
                user_id	integer
                amount	integer
                method	string
              }


### Orders Summary
Get orders made by a user, provided the authorization token in header.

    URL : http://127.0.0.1:9900/api/orders/

    Method : GET


## Docs
The rest of the documentation - Swagger 

    http://127.0.0.1:9900/api/docs/


