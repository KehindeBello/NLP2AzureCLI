import os
from dotenv import load_dotenv

from flask import Flask

app = Flask(__name__)

app.get("/")
def hello_World():
    return "Hello"