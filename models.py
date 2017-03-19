# IMPORTS START
from app import db
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime, date
# IMPORTS END



class User(db.Model):
	__tablename__="users"
	def __init__(self,username,password,first_name,last_name, creation_date):
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
	creation_date = db.Column(db.Date, default = date.today())


class Property(db.Model):

	def __init__(self,building_name, date_updated, coordinates, sq_ft,bedrooms,bathrooms, address, city,state,zipcode,past_price,current_price, status):
		self.building_name = building_name
		self.date_updated = date_updated
		self.coordinates = coordinates
		self.sq_ft = sq_ft
		self.bedrooms = bedrooms
		self.bathrooms = bathrooms
		self.address = address
		self.city = city
		self.state = state
		self.zipcode = zipcode 
		self.past_price = past_price
		self.current_price = current_price
		self.status =  status
		
		
	# SCHEMA
	id = db.Column(db.Integer, primary_key=True)
	building_name = db.Column(db.String(40))
	date_updated = db.Column(db.Date)
	coordinates = db.Column(db.String(50))
	sq_ft = db.Column(db.Float)
	bedrooms = db.Column(db.Float)
	bathrooms = db.Column(db.Float)
	address = db.Column(db.String(100))
	city = db.Column(db.String(30))
	state = db.Column(db.String(20))
	zipcode = db.Column(db.String(30))
	past_price = db.Column(db.Float)
	current_price = db.Column(db.Float)
	status = db.Column(db.String)



class Reference(db.Model):
	__tablename__ = "reference"
	def __init__(self,user_id,prop_id,bedrooms,investment_value):
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
	def __init__(self,lender,total_amount,interest_rate,date_issued):
		self.lender = lender
		self.total_amount = total_amount
		self.interest_rate = interest_rate
		self.date_issued = date_issued
		

	id = db.Column(db.Integer, primary_key=True)
	lender = db.Column(db.String(40))
	total_amount = db.Column(db.Float)
	interest_rate = db.Column(db.Float)
	date_issued = db.Column(db.Date)

# db.drop_all()
# db.create_all()

print("Database has been CREATED")


