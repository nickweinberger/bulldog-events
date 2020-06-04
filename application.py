import os
import re
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, redirect, url_for
from flask_session import Session
import sqlite3
from sqlite3 import Error
from helpers import apology, login_required
from dbfunctions import create_connection, insert_event, get_all_events, search_sports_events, search_acapella_events, search_comedy_events, search_theater_events, convert_date, today_events
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///events.db")

@app.route("/current", methods=["GET", "POST"])
def current():
    # using now() to get current time
    # EventList = []
    # AList = []
    # CList = []
    # TList = []
    # print(request.method)
    # DateList = []
    user_search=""
    if request.method == "POST":
        # now = datetime.datetime.now()
        # m = str(now.month)
        # d = str(now.day)
        # y = str(now.year)
        # c_date = m + "/" + d + "/" + y
       # print(request.form)
       # if request.form["submit_button"] in request.form:
          #  print("Hello")
        #c_date = "12/08/2019"
       # print(c_date)
       # DateList = today_events(c_date)
        details = request.form
        # print(request.form)
        #if exists, python gets the value of key in dict
        if details.get('Search'):
         user_search = details["Search"]
        # print("test dd1")
        # input_date = details["submit_button"]
        #x = date["datepicker"]
        #print(date)
    EventList = search_sports_events(user_search,"current")

    AList = search_acapella_events(user_search,"current")
    CList = search_comedy_events(user_search,"current")
    TList = search_theater_events(user_search,"current")
    EventList.extend(AList)
    EventList.extend(CList)
    EventList.extend(TList)
    print(EventList)
        # print(request.form)
        # Flask.redirect("/")
        # if request.form["Search"] in request.form:
        #     user_search = request.form["Search"]
        #     EventList = search_sports_events(user_search)
        #     AList = search_acapella_events(user_search)
        #     CList = search_comedy_events(user_search)
        #     TList = search_theater_events(user_search)
        #     EventList.extend(AList)
        #     EventList.extend(CList)
        #     EventList.extend(TList)


    return render_template("home.html", EventList = EventList)

@app.route("/later", methods=["GET", "POST"])
def later():
    user_search=""
    if request.method == "POST":
        details = request.form
        # print(request.form)
        #if exists, python gets the value of key in dict
        if details.get('Search'):
         user_search = details["Search"]
    EventList = search_sports_events(user_search,"later")

    AList = search_acapella_events(user_search,"later")
    CList = search_comedy_events(user_search,"later")
    TList = search_theater_events(user_search,"later")
    EventList.extend(AList)
    EventList.extend(CList)
    EventList.extend(TList)
    return render_template("home.html", EventList = EventList)


#https://support.theeventscalendar.com/153124-Themers-Guide
#display this on homepage instead
@app.route("/", methods=["GET", "POST"])
def home():
    AList = []
    EventList = []
    AList = []
    CList = []
    TList = []
    user_search=''
    if request.method == "POST":
        details = request.form
        user_search = details["Search"]
        # input_date = details["submit_button"]
        #x = date["datepicker"]
        #print(date)
    EventList = search_sports_events(user_search,"")
    AList = search_acapella_events(user_search,"")
    CList = search_comedy_events(user_search,"")
    TList = search_theater_events(user_search,"")
    EventList.extend(AList)
    EventList.extend(CList)
    EventList.extend(TList)
    return render_template("home.html", EventList = EventList)

@app.route("/sports", methods=["GET", "POST"])
def sports():
    EventList = []
    if request.method == "POST":
        details = request.form
        user_search = details["Search"]
        EventList = search_sports_events(user_search,"")
    return render_template("sports.html", EventList = EventList)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Must provide password")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("Invalid username and/or password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/add_event")


    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Must provide username")

        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("Must provide password")

        # Ensure confirmation was submitted
        if not request.form.get("confirmation"):
            return apology("Must provide confirmation")

        # Ensure confirmation matches password
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("Confirmation must match password")

        # Ensure password meets requirements
        password = request.form.get("password")
        if any(i.isdigit() for i in password) is False:
            return apology("Password must be at least eight characters long and include at least one number and character")
        if any(i.isalpha() for i in password) is False:
            return apology("Password must be at least eight characters long and include at least one number and character")
        if len(password) < 8:
            return apology("Password must be at least eight characters long and include at least one number and character")

        # Query database for username
        rows = db.execute("SELECT username FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # If username already exists, return apology
        if len(rows) > 0:
            return apology("Username is already taken")

        # Insert registration data into users table
        password = generate_password_hash(request.form.get("password"))
        username = request.form.get("username")
        try:
            db.execute("INSERT INTO users (username, hash) VALUES (:username, :password)", username=username, password=password)
        except:
            print("FAILURE")

        # Remember which user has logged in
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"));

        session["user_id"] = rows[0]["id"]

        # Redirect user to add_event page
        return redirect("/add_event")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")

@app.route("/add_event", methods=["GET", "POST"])
@login_required
def add_event():
    if request.method == "POST":
        details = request.form

        Sport_name = details["Sport_type"]
        Sport_gender = details["Gender"]
        Sport_opposing_team = details["Opposing_team"]

        Event_name = "{}'s {} vs. {}".format(Sport_gender, Sport_name, Sport_opposing_team)
        print(Event_name)
        Event_date = details["Event_date"]
        date = details["Event_date"]
        date = date.split("-",2)
        date = list(map(int, date))

        #conv_Event_Date is the name of the actual sql column we can query for date time
        conv_Event_date = convert_date(date)
        print(conv_Event_date)
        if len(Event_date) == 9:
            Event_date = "0" + Event_date

        Event_address = details["Event_address"]
        Event_time = details["Event_time"]
        Event_description = details["Event_description"]
        Event_ticket_link = details["ticket_link_here"]
        Event_image = details["Image"]
        insert_event(Event_date, Event_time, Event_description, Event_address, Event_ticket_link, Event_image, conv_Event_date, Event_name)
        get_all_events()
    return render_template("add_event.html")

@app.route("/comedy", methods=["GET", "POST"])
def comedy():
    """Comedy events page"""
    EventList = []
    if request.method == "POST":
        details = request.form
        user_search = details["Search"]
        EventList = search_comedy_events(user_search,"")
        print(EventList)
    return render_template("comedy.html", EventList = EventList)

@app.route("/theater", methods=["GET", "POST"])
def theater():
    """Theater events page"""
    EventList = []
    if request.method == "POST":
        details = request.form
        user_search = details["Search"]
        EventList = search_theater_events(user_search,"")
    return render_template("theater.html", EventList = EventList)

@app.route("/acapella", methods=["GET", "POST"])
def acapella():
    EventList = []
    if request.method == "POST":
        details = request.form
        user_search = details["Search"]
        EventList = search_acapella_events(user_search,"")
        print(EventList)
    return render_template("acapella.html", EventList = EventList)


app.run(host='0.0.0.0')