# FastAPI Cleaning Reports
## Introduction

This server is built using `FastAPI` and interacts with `MongoDB` to manage cleaning reports on `FLEXA`.

## Setup

You will first need to create a `.env` file to define the environment variables this app will use to run. Following `.env.example`:

```
PORT=<port number>
DEBUG_MODE=<True for development and False for production>
DATABASE_NAME=<name of database>
DATABASE_URL=<mongodb url>
```

You will also need to install `Python` packages listed in `Pipfile/requirements.txt`. 

### Using pipenv (recommended)

Run the following commands to create a virtual environment for this project:

```
# creates .venv folder in current directory
mkdir .venv

OR

# installs from Pipfile
pipenv install 
```

### Using pip

Without virtual environment:

```
# installs from requirments.txt
pip install -r requirements.txt
```

## Running the app

### Using virtual environment

To use the virtual environment (`.venv`) created:

```
# without pipenv shell
pipenv run python app/main.py

OR

# with shell
pipenv shell
python run app/main.py

# to exit pipenv shell
deactivate
```

### Without virtual environment

Running the app using your global `Python` interpreter:

```
python app/main.py
```

## Swagger UI

`FastAPI` comes with `Swagger UI` to call and test your API directly from the browser. You may access the this UI at [Swagger UI](http://localhost:8092/docs) (this assumes that the app is running on `localhost:8092`).

![image-20230220131650142](/home/russ1337/snap/typora/76/.config/Typora/typora-user-images/image-20230220131650142.png)

