# involve-test

## Prerequisites
- Python 3.7
- Flask 1.1.2

## If you want to run server you need to do next steps:
- create venv
- run ```pip install -r requirements.txt```
- run ```flask db upgrade```
- start server with ```gunicorn --bind  {host}:{port} app:app```
