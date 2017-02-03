# shufflebox-backend

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
    DB_USER=posgres
    DB_PASSWORD=<Your-password>
    ```

    Save the file. You'll need it to keep sensitive info from the outside world, and make migrations work! 😄

* #### Migrations
    On your psql console, create your database:
       ```
       > CREATE DATABASE shufflebox;
       ```
    Then, make your Migrations
       ```
       $ python3 manage.py makemigrations
       ```

    And finally, migrate your migrations to persist on the DB
       ```
       $ python3 manage.py migrate
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

## Contributing
TBD
