from flask import Flask, request, render_template, make_response, session
from flask_session import Session
import random
import uuid
import os
from bot import bot

HOST_NAME = "http://127.0.0.1:8080"

app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(64)

Users = {}


@app.route('/getcookie', methods=['POST', 'GET'])
def setcookie():
    # this is just to generate a random userId
    user = str(uuid.uuid4())
    session["userId"] = user
    R = random.Random()
    Users[user] = R
    resp = make_response(
        f"your cookie has been set use it now to continue the challenge and your unique id is : {user}")
    return resp


@app.route("/hello")
def hello_world():
    try:
        user = session["userId"]
    except:
        user = request.args.get("userId", '')
    msg = request.args.get('msg', '')
    if user is None:
        return "You did not set any cookie go back to main page and set one"
    elif user not in Users:
        return "the userId you entered is no set go to /getcookie to take your cookie and set a new userId"
    else:
        R = Users[user]
    nonce = hex(R.getrandbits(32))[2:]

    resp = make_response(f"<p>Hello, {msg}</p>")
    resp.headers['Content-Security-Policy'] = f"script-src 'nonce-{nonce}';"

    return resp


@app.route("/report", methods=['POST', 'GET'])
def report():
    if request.method == "POST":
        url = request.form.get("url")
        result = bot.visit_report(url)
        return result
    elif request.method == "GET":
        return render_template("bot.html", url=HOST_NAME+"/report")


@app.route("/")
def home():
    return """
    <html>
    <head>
        <title>KrySS</title>
    </head>

    </body>

        <h1>
            this is just a simple XSS chall :)
        </h1>
    <h3> And because im a good person i will give you free cookies </h3>
    <form action="/getcookie" method="POST">
            <p>
            <h3>Click to get one </h3>
            </p>
            <p><input type='submit' value='getcookie' /></p>
        </form>
        
    </html>
    """


app.run(host="0.0.0.0", port="8080")
