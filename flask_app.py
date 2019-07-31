from flask import Flask, render_template, session, redirect, url_for, escape, request
import sqlite3
import hashlib, os, binascii
from os import path

#---setting up App

app = Flask(__name__)
app.secret_key = 'any random stringgg'

#---setting up Database (sqlite)

ROOT = path.dirname(path.realpath(__file__))
conn = sqlite3.connect(path.join(ROOT,"Hackathon.db"))
c = conn.cursor()

#c.execute("CREATE TABLE IF NOT EXISTS Guests( Guest_id INTEGER PRIMARY KEY AUTOINCREMENT, First_name TEXT NOT NULL, Last_name TEXT NOT NULL, Email_address TEXT NOT NULL, Level INTEGER DEFAULT 0 NOT NULL, Username TEXT NOT NULL, Password TEXT NOT NULL);")
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
 
        First_name = request.form.get("firstname")
        Last_name = request.form.get("lastname")
        Email_address = request.form.get("email")
        Username = request.form.get("username")
        Password = request.form.get("password")
        Password = hash_password(Password)  #hashing the password

        if Username_exists(Username):
            return render_template("message.html", message = "Username already exists", desto="/register")

        c.execute("INSERT INTO Guests (First_name, Last_name, Email_address, Username, Password) values (?, ?, ?, ?, ?)",(First_name, Last_name, Email_address, Username, Password))
        conn.commit

        session['username'] = Username
        return redirect("/")

    return render_template('register.html', output = "Guest")

@app.route('/login', methods=["POST","GET"] )
def login():

    output = "Guest"

    if request.method == 'POST':
        Username = request.form.get("username")
        Password = request.form.get("password")
        c.execute("SELECT Username FROM Guests")
        conn.commit()
        rows=c.fetchall()
        usernames = []
        for row in rows:
            usernames.append(row[0])
        if Username not in usernames:
            return render_template("message.html", message = "No such user", desto="/login")

        c.execute("SELECT Password FROM Guests WHERE Username = '%s'" % Username)
        conn.commit()
        rows=c.fetchall()

        stored_password = ""
        for row in rows:
            stored_password = row[0]

        provided_password = Password

        if verify_password(stored_password, provided_password):
            print("Logged in succesfully !")
            session['username'] = Username
            return redirect("/")
        else :
            return render_template("message.html", message = "Passwords don't match", desto="/login")



    return render_template('login.html')
 
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect("/login")

@app.route('/showguests')
def showguests():

    if 'username' not in session:
        return render_template("message.html", message = "Must be logged in as admin", desto="/login")
    if session['username'] != "admin":
        return render_template("message.html", message = "Must be logged in as admin", desto="/login")
    
    output = "Welcome admin !"

    c.execute("SELECT * FROM Guests ORDER BY Last_name")
    conn.commit()
    rows=c.fetchall()

    return render_template('showguests.html', rows=rows , output = output)



#---functions without routing

def Username_exists(Username):
    c.execute("SELECT Username FROM Guests")
    conn.commit()
    rows=c.fetchall()
    usernames = []
    for row in rows:
        usernames.append(row[0])
    if Username not in usernames:
        return False
    else:
        return True

def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')
 
def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                  provided_password.encode('utf-8'), 
                                  salt.encode('ascii'), 
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password
