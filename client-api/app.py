import requests
from flask import Flask

app = Flask(__name__)

@app.route("/getUsers")

def clientApi():
    usersData = requests.get("http://server-api:5000/users").json()
    return usersData
