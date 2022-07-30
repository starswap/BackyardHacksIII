from flask import Blueprint, render_template, session, redirect, url_for
from arcadia.arcadiaApp.requiremobile import requiremobile
from flask import Blueprint, request
from passlib.hash import argon2
from requests import Response
from arcadia.db import get_db
from arcadia.arcadiaApp.requiremobile import requiremobile

# from flask import current_app as app

app_bp = Blueprint('app_bp', __name__, template_folder="templates", static_folder="static", static_url_path="/ast")

@app_bp.route('/')
@requiremobile
def home():
    if session.get("userid"):
        return render_template("displayguesses.jinja2")
    else:
        return render_template("displayguesses.jinja2")



@app_bp.route('/register', methods=["GET","POST"])
@requiremobile
def account():

    if request.method == 'GET':
        return render_template("register.jinja2")

    elif request.method == 'POST':
        username = request.values.get('username')
        password = request.values.get('password')
        hashed_password = argon2.hash(password)

        db, cur = get_db()
        cur.execute("""INSERT INTO 'Users' (UserName, PasswordHash) VALUES (%s,%s);""",
        (username, hashed_password))
        return redirect(url_for("app_bp.home"))


@app_bp.route('/login', methods=["GET","POST"])
@requiremobile
def login():

    if request.method == 'GET':
        return render_template("login.jinja2",)

    elif request.method == 'POST':
        username = request.values.get('username')
        password = request.values.get('password')
        hashed_password = argon2.hash(password)
        
        db, cur = get_db()
        cur.execute("""SELECT PasswordHash FROM 'Users' WHERE UserName= %s;""", (username,))
        resp = cur.fetchone()
        if resp == None:
            return redirect(url_for("account_bp.login"))
        if not argon2.verify(password, resp["PasswordHash"]):
            return redirect(url_for("account_bp.login"))
        else:

            #NOT SURE HOW TO AUTHENTICATE WITH COOKIE OR EQUIVELANT
            pass


        
    return Response(
        status = 200,
        mimetype='application/json'
    )