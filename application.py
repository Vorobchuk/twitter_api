from flask import Flask, render_template, request
from twitter2 import map_create, name_loc

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route("/")
def page():
    return render_template("user.html")


@app.route("/", methods=["POST", "GET"])
def showing_map():
    user = request.form["name"]
    data = name_loc(user)
    return map_create(data)


