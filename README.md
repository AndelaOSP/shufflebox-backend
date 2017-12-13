# shufflebox-backend
[![Build Status](https://travis-ci.org/AndelaOSP/shufflebox-backend.svg?branch=develop)](https://travis-ci.org/AndelaOSP/shufflebox-backend)

## Overview
A Django-powered API for handling shufflebox consumption client requests

## Technologies used
* [Django](https://www.djangoproject.com/): The web framework for perfectionists with deadlines (Django builds better web apps with less code).
* [Django Rest Framework](http://www.django-rest-framework.org/): A powerful and flexible toolkit for building web APIs.
* Minor dependencies can be found in the requirements.txt file on the root folder.


## Installation / Usage
* If you wish to run your own build, first ensure you have python3 globally installed in your computer. If not, you can get python3 [here](https://www.python.org).
* After this, ensure you have installed virtualenv globally as well. If not, run this:
    ```
        $ pip install virtualenv
    ```
* Git clone this repo to your PC
    ```
        $ git clone git@github.com:AndelaOSP/shufflebox-backend.git
    ```


* #### Dependencies
    1. Cd into your the cloned repo as such:
        ```
        $ cd shufflebox-backend
        ```

    2. Create and fire up your virtual environment in python3:
        ```
        $ virtualenv -p python3 env
        $ source env/bin/activate
        ```
    3. Install dependencies stored in the requirements text file:
        ```
        $ pip install -r requirements.txt
        ```

* #### Environment Variables
    Create a .env file and add the following:
    ```
    SECRET_KEY=<Your-Secret-Key>
    DB_USER=<Your-username>
    DB_PASSWORD=<Your-password>
    JWT_TOKEN=<YOUR JWT TOKEN>
    DJANGO_SETTINGS_MODULE=<Path to settings file e.g core.settings.production>
    USER_API_TOKEN=<Bearer token>
    USER_SERVICE_URL=<url-for-andela-user-microservice>
    FILTER_PARAMS=<filter-to-query-users-from-microservice>
    EMAIL_USE_TLS=<EMAIL TLS>
    EMAIL_HOST=<EMAIL HOST>
    EMAIL_PORT=<EMAIL PORT>
    EMAIL_HOST_USER=<EMAIL USER ADRESS>
    EMAIL_HOST_PASSWORD=<EMAIL USER PASSWORD>
    DEFAULT_FROM_EMAIL=<DEFAULT FROM EMAIL ADDRESS> e.g SHUFFLEBOX <shuffle@andela.com>
    ```

    Save the file. You'll need it to keep sensitive info from the outside world, and make migrations work! 😄

* #### Migrations
    On your psql console, create your database:
       ```
       > CREATE DATABASE core;
       ```

    Then, make your Migrations
       ```
       $ python3 manage.py makemigrations
       ```

    Migrate your migrations to persist on the DB
       ```
       $ python3 manage.py migrate
       ```
       
    Finally, add seed data to your newly created database
    - Required: Admin user for shufflebox(P&C)
     ```
     $ python3 manage.py loaddata admin.json
     ```
    - Optional: Initial data to populate your db
     ```
     $ python3 manage.py loaddata initial_data.json
     ```
    

* #### Running It
    On your terminal, run the server using this one simple command:
    ```
    $ python3 manage.py runserver
    ```
    You can now access the app on your local browser by using
    ```
      http://localhost:8000/
    ```

### Available Endpoints

| Endpoint                    | Description                                                                    |
| --------------------------  | ------------------------------------------------------------------------------ |
| [POST /api/shuffle/](#)     | Shuffle according to request. Request contains **_"type"_**:("hangout" or "brownbag" or "secretsanta") and **_"limit"_**: (Integer) in raw json format|
| [GET /api/users/](#)        | Get a list of users. |
| [GET /api/users/:id](#)     | Get a single profile for a user using a user ID. |
| [POST /api/brownbags/](#)   | Create a single brownbag. Request should have **_date_**, **_status_** and **_user_id_** in form data |
| [GET /api/brownbags/](#)    | Get a list of all created brownbags, inclusive of the one next-in-line. |
| [GET /api/brownbags/:id](#) | Get a single brownbag. |
| [PUT /api/brownbags/:id](#) | Update a single brownbag. |
| [DELETE /api/brownbags/:id](#) | Delete a single brownbag. |
| [GET /api/brownbags/next/](#) | Get the next brownbag presenter. |
| [GET /api/brownbags/not_presented/](#) | Get all users who have not presented a brownbag. |
| [POST /api/hangouts/](#) | Create a single hangout group. Request should have _date_ and _members_ in form or raw json data. |
| [GET /api/hangouts/](#) | Get all created hangout groups. |
| [GET /api/hangouts/:id](#) | Get a single hangout group using its id. |
| [PUT /api/hangouts/:id](#) | Update a single hangout group. Request should have _date_ and _members_ in form or raw json data. |
| [DELETE /api/hangouts/:id](#) | Delete a single hangout group. |
| [POST /api/santas/](#) | Create a single Secret Santa pair. |
| [GET /api/santas/](#) | Get a list of all Secret Santa pairs. |
| [GET /api/santa/:id](#) | Get a single Secret Santa pair. |
| [POST /api/mail/](#) | Send out shuffle box emails. Request contains **_"type"_**:("hangout" or "brownbag" or "secretsanta") |
| [GET /api/giftee/](#) | Get the giftee of the logged in user |


## Contributing
TBD
