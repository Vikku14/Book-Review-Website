import os

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

os.environ["DATABASE_URL"] = "postgres://thsglqrnqzkafm:a2bfd93\
866f5e5e91d9f7e88a6223ba9e0081160c544226cdb83e4bffbc53aff@ec2-10\
7-21-216-112.compute-1.amazonaws.com:5432/d1e20ma3mf0vn9"

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("home.html")

@app.route("/login")
def signin():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

# @app.route("/Home1", methods=["POST"])
# def signedup():
# 	name = request.form.get("name")
# 	password = request.form.get("pass")
# 	# TODO execute
# 	result=name
	

@app.route("/<string:hometype>", methods=["POST"])
def logedup(hometype):
	name = request.form.get("name")
	password = request.form.get("pass")
	# TODO execute
	print("login ",hometype,"\n \n")
	result=name
	if hometype == "LoginHome":
		if db.execute("select * from users where loger=:name",{"name":name}).rowcount == 0:
			return render_template("login.html",message="User Doesn't exist.")
		else:
			data = db.execute("select * from books").fetchall()
			return render_template("final.html",result=result, data = data)
	if hometype == "SignHome":
		print("entered signedin \n \n")
		if db.execute("select * from users where loger=:name",{"name":name}).rowcount == 0:
			db.execute("INSERT INTO users(loger, password) VALUES(:name, :password)",{"name": name, "password": password})
			db.commit()
			data = db.execute("select * from books limit 10").fetchall()
			return render_template("final.html",result=result, data=data)
		else:
			return render_template("signup.html",message="User already exists.")
		