# Awesome Cart

# Getting Started

First clone the repository from Github and switch to the new directory:
  ```shell
    $ gh repo clone charitraa/StoreFront
    $ cd StoreFront
  ```

## Installation

Python 3.4 is required. If you don't have Python 3.4 or higher, download the appropriate package and install:

```shell
wget https://www.python.org/ftp/python/3.4.3/python-3.4.3-macosx10.6.pkg
```

Then install virtualenv:

```shell
sudo pip3 install virtualenv
```

Create a virtualenv for StoreFront and activate it:

```shell
virtualenv -p <PYTHON_3_PATH> ~/virtualenvs/StoreFront
source ~/virtualenvs/StoreFront/bin/activate
```

Install Django into the virtualenv:

```shell
~/virtualenvs/StoreFront/bin/pip3 install Django
```
    
Activate the virtualenv for your project.
    
Now, install the rest of the packages that are required by your Django project:
  ```shell
~/virtualenvs/StoreFront/bin/pip3 install -r requirements.txt
  ```
    
Setup the database. Locally, this will create a new sqllite database
```shell
~/virtualenvs/StoreFront/bin/python3 manage.py migrate
    OUTPUT:
Operations to perform:
  Apply all migrations: contenttypes, sessions, admin, auth
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying sessions.0001_initial... OK
```

Start the Django server:

```shell
~/virtualenvs/StoreFront/bin/python3 manage.py runserver
```

Your Django project is now live, locally. In your browser, go to: http://localhost:8000.
