# Space Observatory API

Database-backed REST API built with FastAPI and SQL for observing celestial bodies and recording the observations. 

Developed wtih assistance from Codex 5.6 SOL

## How to run:

### Install dependencies:

1. Open PowerShell command bar
2. Type `py -m pip install -r requirements.txt`

### Start the Server:
1. Type `py -m uvicorn main:app --reload`
2. Type `/docs` at the end of the URL bar

## Project Structure

``` text
space-observatory-api/
|-- database.py
|-- DEVLOG.md
|-- main.py
|-- README.md
|-- requirements.txt
|-- schemas.py
`-- tests/
    `-- test_api.py