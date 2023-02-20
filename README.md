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

`FastAPI` comes with `Swagger UI` to call and test your API directly from the browser. You may access  `Swagger UI` at [http://localhost:8092/docs](http://localhost:8092/docs) (this assumes that the app is running on `localhost:8092`).

![image](https://user-images.githubusercontent.com/88697228/220016403-58409aea-9b1f-42d6-8f3b-e4987c6c4768.png)

