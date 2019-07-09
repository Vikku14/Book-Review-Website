import os
import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

os.environ["DATABASE_URL"] = "postgres://thsglqrnqzkafm:a2bfd93\
866f5e5e91d9f7e88a6223ba9e0081160c544226cdb83e4bffbc53aff@ec2-10\
7-21-216-112.compute-1.amazonaws.com:5432/d1e20ma3mf0vn9"

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


def main():
	f= open("books.csv")
	reader = csv.reader(f)
	# delete schema of table from books.csv
	# Create table manually.
	for i, t, a , y in reader:
		db.execute("Insert into books (isbn, title, author, year) Values (:i, :t, :a, :y)",{'i':i,'t':t, 'a':a, 'y': y})
		print(f"Added {i}")
	db.commit()

if __name__ == '__main__':
 	main()