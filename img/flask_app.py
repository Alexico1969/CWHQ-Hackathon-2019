from flask import Flask, render_template, session, redirect, url_for, escape, request
import sqlite3
from os import path

#---setting up App

app = Flask(__name__)
app.secret_key = 'any random stringgg'

#---setting up Database (sqlite)

ROOT = path.dirname(path.realpath(__file__))
conn = sqlite3.connect(path.join(ROOT,"Hackathon.db"))
c = conn.cursor()

#c.execute("CREATE TABLE IF NOT EXISTS Guests( Guest_id INTEGER PRIMARY KEY AUTOINCREMENT, First_name TEXT NOT NULL, Last_name TEXT NOT NULL, Email_address TEXT NOT NULL, Level INTEGER DEFAULT 0 NOT NULL, Username  TEXT NOT NULL, Password  TEXT NOT NULL);")
#c.execute("CREATE TABLE IF NOT EXISTS Levels( Level_id INTEGER PRIMARY KEY, Name TEXT NOT NULL, Badge_color TEXT NOT NULL, Img BLOB, Text TEXT NOT NULL, Answer TEXT NOT NULL, Release_date TEXT NOT NULL);")


@app.route('/')
def index():
    if 'username' in session:
        username = session['username']
        output= 'Logged in as ' + username
    else:
        output = "Guest"
        return redirect("/register")
    return render_template('home.html', output = output)

@app.route('/register', methods=["POST","GET"] )
def register():

    if request.method == 'POST':
        if Username_exists():
            return render_template("message.html", message = "Username already exists")

    return render_template('register.html', output = "Guest")


#---functions without routing

def Username_exists():
    print("todo")
    return
