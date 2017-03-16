# IMPORTS START
from app import db
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
# IMPORTS END

db.drop_all()

class User(db.Model):
	def __init__(self,id,username,password,first_name,last_name, creation_date):
		self.id = id
		self.username = username
		self.password = password
		self.first_name = first_name
		self.last_name = last_name
		self.creation_date = creation_date
		
		

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(40), unique=True)
	password = db.Column(db.String(200))
	first_name = db.Column(db.String(40))
	last_name = db.Column(db.String(40))
	creation_date = db.Column(db.String(20), default = datetime.today())


class Property(db.Model):

	def __init__(self,id,building_name,sq_ft,bedrooms,bathrooms, address, city,zipcode,past_price,current_price, status):
		self.id = id
		self.building_name = building_name
		self.sq_ft = sq_ft
		self.bedrooms = bedrooms
		self.bathrooms = bathrooms
		self.address = address
		self.city = city
		self.zipcode = zipcode 
		self.status =  status
		
		
	# SCHEMA
	id = db.Column(db.Integer, primary_key=True)
	building_name = db.Column(db.String(40), primary_key=True)
	sq_ft = db.Column(db.Float, primary_key=True)
	bedrooms = db.Column(db.Float, primary_key=True)
	bathrooms = db.Column(db.Float, primary_key=True)
	address = db.Column(db.String(100))
	city = db.Column(db.String(30))
	zipcode = db.Column(db.String(30))
	past_price = db.Column(db.Float)
	current_price = db.Column(db.Float)
	status = db.Column(db.String)



class Reference(db.Model):
	__tablename__ = "reference"
	def __init__(self,id,user_id,prop_id,bedrooms,investment_value):
		self.id = id
		self.user_id = user_id
		self.prop_id = prop_id
		self.mortgage_id = mortgage_id
		self.investment_value = investment_value
		
	# SCHEMA
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer)
	prop_id = db.Column(db.Integer)
	mortgage_id = db.Column(db.Integer)
	investment_value = db.Column(db.Float)
	

class Mortgage(db.Model):
	__tablename__ = "mortgage"
	def __init__(self,id,lender,total_amount,interest_rate,date_issued):
		self.id = id
		self.lender = lender
		self.total_amount = total_amount
		self.interest_rate = interest_rate
		self.date_issued = date_issued
		

	id = db.Column(db.Integer, primary_key=True)
	lender = db.Column(db.String(40))
	total_amount = db.Column(db.Float)
	interest_rate = db.Column(db.Float)
	date_issued = db.Column(db.Date)


db.create_all()

print("Database has been CREATED")


