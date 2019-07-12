import os
import requests
from math import ceil
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

def finalPage():
	return db.execute("select * from books order by year desc limit 10 ").fetchall()

@app.route("/<string:hometype>", methods=["GET","POST"])
def logedup(hometype):
	if request.method == 'GET':
		return render_template('Notallowed.html')
	else:
		name = request.form.get("name")
		password = request.form.get("pass")
		
		session["user"] = name
		if hometype == "LoginHome":
			if db.execute("select * from users where loger=:name and password=:password",{"name":name,
				"password":password}).rowcount == 0:
				return render_template("login.html",message="User/Password Doesn't exist.")
			else:
				data = finalPage()
				return render_template("final.html",result=session["user"], data = data,res = "latest books")

		if hometype == "SignHome":
			if db.execute("select * from users where loger=:name",{"name":name}).rowcount == 0:
				db.execute("INSERT INTO users(loger, password) VALUES(:name, :password)",{"name": name, "password": password})
				db.commit()
				data = finalPage()
				return render_template("final.html",result=session["user"], data = data, res = "latest books:")

			else:
				return render_template("signup.html",message="User already exists.")

@app.route("/Home/Search", methods=["GET","POST"])
def find():
	if request.method == "GET":
		return render_template('Notallowed.html')
	else:
		res = request.form.get("search")
		res = '%'+res.lower()+'%'
		# print(res)
		data = db.execute("select * from books where lower(isbn) like :res or lower(title) like :res or lower(author)\
			like :res order by year desc",{'res':res}).fetchall()
		if len(data) == 0:
			return render_template("final.html",result=session["user"], data = "", res=
				"Search result: '"+res[1:-1]+"'")	
		else:
			return render_template("final.html",result=session["user"], data = data,
				res="Search result: '"+res[1:-1]+"'")

@app.route("/Home/AllBooks")
def allbooks():
	data = db.execute("select * from books order by year desc").fetchall()
	print(data)
	return render_template("final.html",result=session["user"], data = data)


@app.route("/Home/detail/<string:isbn>",methods=["GET","POST"])
def detail(isbn):
	# API used
	res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "duJuPv6MUWcUjUKpV3CUJg",
 	"isbns": isbn})
	k =res.json()
	comment = request.form.get("comment")
	rate= request.form.get("rating")

	if (comment is not None and comment != '') and \
	 db.execute(" select * from reviews where isbn=:isbn and loger=:loger",
	 	{'isbn':isbn, 'loger':session["user"]}).rowcount == 0 :
		db.execute("insert into reviews values (:isbn, :user, :comment, :rate)",{'isbn': isbn, 'user':session["user"],
			'comment':comment, 'rate':rate})
		db.commit()
	reviews = db.execute("select * from reviews where isbn=:isbn",{'isbn': isbn}).fetchall()
	db.commit()
	tab = list()
	tab.append(k['books'][0]['work_ratings_count'])
	tab.append(k['books'][0]['average_rating'])
	tab.append(k['books'][0]['isbn'])

	x = ceil(float(tab[1]))

	book_result = db.execute("select * from books where isbn= :isbn",{'isbn':isbn})
	return render_template("detail.html",goodreads = tab, book_result = book_result,
			reviews= reviews,x = x)

@app.route("/api/<string:isbn>")
def getisbn(isbn):
	try:
		res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "duJuPv6MUWcUjUKpV3CUJg",
	 	"isbns": isbn})
		k =res.json()
		data = db.execute("select * from books where isbn = :isbn",{'isbn':isbn}).fetchall()
		tab = list()
		print(data)
		tab.append(data[0][1])
		tab.append(data[0][2])
		tab.append(data[0][3])
		tab.append(data[0][0])

		tab.append(k['books'][0]['work_ratings_count'])
		tab.append(k['books'][0]['average_rating'])

		return render_template("jsonfile.html",data=tab )
	except:
		return render_template("error.html")
