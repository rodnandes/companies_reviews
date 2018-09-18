# Reviews API

This project is an API that Users can submit reviews to companies, developed with Python, Django and the Django Rest Framework.

## Setup

Make sure that you have Python 3.6+ installed on your system, then install the project dependecies. You may do it using Python's `virtualenv` for this particular project for convinience.

```bash
virtualenv -p python3.6 <YOUR_VENV_NAME>
```

Activate your virtual environment:

```bash
source ./<YOUR_VENV_NAME>/bin/activate
```

### Requirements:

The essential project requirments are:

- Django 2.1+
- Django Rest Framework 3.8+

You can install them from the `requirements.txt` with `pip` file as follows:

```bash
pip install -r ./requirements.txt
```

### Running the project

To run the project, you will need to migrate the database schema.

```bash
./manage.py makemigrations &&
./manage.py migrate
```

You can create a superuser as well:

```bash
./manage.py createsuperuser
```

Add your credentials as needed.

Then you may run the development server:

```bash
./manage.py runserver
```

You can check the application running on `http://localhost:8000/`.`

## API Usage

To access the API you will need to get a token for your User.

You can register a new user, and get the token providing the User's credentials.

### Registration, Login and Access Token

Before effectively using the API, you will need to register a User and get its access Token.

You can login to the API sending requests via `curl`.

First, register a new User:

```bash
curl -X POST -d "username=someuser&password=secret123&email=me@email.com" localhost:8000/api/register/
```

Then login with the created user registration to get the access token:

```bash
curl -X POST -d "username=someuser&password=secret123" localhost:8000/api/login/
```

Once you logged the API will send a response with the access token for the User.

