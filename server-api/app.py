import requests
from flask import Flask

app = Flask(__name__)

@app.route("/users")

def serverApi():
    users = requests.get("https://jsonplaceholder.typicode.com/users").json()
    return users
