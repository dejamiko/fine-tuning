# Translator

This is an app utilising the models I trained for my final year project.

It is a simple Django app, with simple user management. It allows translating between English and Polish, both ways. 
It also stores past translations for logged-in users.

## Installation
To install the app, you need to have Python 3 installed (3.9 recommended). Then, you need to install the requirements:

    virtualenv venv --python=3.9
    source venv/bin/activate
    pip3 install -r requirements.txt

Then, you need to create a database:

    python3 manage.py migrate

Then, you need to run the server:

    python3 manage.py runserver

To run tests, use the following command:

    python3 manage.py test

To run coverage, use the following command:

    coverage run manage.py test
    coverage report

## Usage
To use the app, navigate to `localhost:8000` in your browser. 
You can then register an account, and log in if you choose to do so. 
You can translate between English and Polish, both ways.