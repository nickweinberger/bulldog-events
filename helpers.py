import os
import requests
import re
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
import sqlite3
from sqlite3 import Error
from functools import wraps

def apology(message):
    """Render message as an apology to user."""

    return render_template("apology.html", bottom=(message))


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function