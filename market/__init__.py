from flask import Flask
from flask_cors import CORS
from psycopg2 import connect

import os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(dotenv_path=Path("env\.env"))
app = Flask(__name__)
# app = Flask(__name__, static_folder='build/')


try:
    params = {
        'dbname':os.getenv("DBNAME"),
        'user':os.getenv("USER"),
        'password':os.getenv("PASSWORD"),
        'host':os.getenv("DBHOST"),
        'port':os.getenv("DBPORT")
    }
    connection = connect(**params)
    cursor = connection.cursor()
    print("Connected to database.")
except Exception as e:
    print("Connection Error:", e)


CORS(app, supports_credentials=True)

from market import routes