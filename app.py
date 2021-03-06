# IMPORTS START
from config import DevConfig
from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime, date
import json
import random
from models import *
from uhoh import uhoh



# IMPORTS END


app = Flask(__name__)

app.config.from_object("config.DevConfig")

# generated_secret_key

app.secret_key = "ssshhhh"


db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

def grab_other_investors(prop_id):
	reference_list = db.session.query(Reference).filter(Reference.prop_id==prop_id, Reference.user_id!=session['user_id']).all()
	list_of_investors = []
	for reference in reference_list:
		investment_value = reference.investment_value
		investor = User.query.filter_by(id = reference.user_id).first()
		investor_obj = {"name": investor.username, "amount": investment_value}
		list_of_investors.append(investor_obj)
	return list_of_investors




def grab_saved_and_invest_property():
	user_reference_list = Reference.query.filter_by(user_id=session['user_id']).all()
	invested_properties = []
	saved_properties = []
	for user_reference in user_reference_list:
		if user_reference.investment_value > 0:
			invested_property = Property.query.filter_by(id = user_reference.prop_id).first()
			invested_properties.append(invested_property)
		if user_reference.investment_value == 0:
			saved_property = Property.query.filter_by(id = user_reference.prop_id).first()
			saved_properties.append(saved_property)
		else:
			pass

	return [invested_properties,saved_properties]



def check_property_invested(property_obj, total_property_list):
	invested_properties = total_property_list[0]




def grab_users_properties():
	reference_list = Reference.query.filter_by(user_id=session['user_id']).all()
	property_id_list = []
	for reference in reference_list:
		property_id_list.append(reference.prop_id)
	properties = []
	for prop_id in property_id_list:
		result = Property.query.filter_by(id=prop_id).first()
		if result:
			properties.append(result)
		else:
			print("no result")
	return properties




def session_set(user):
	session.clear()
	session['logged-in'] = True
	session['user_id'] = user.id
	session['username'] = user.username
	print('username is ' + user.username)
	session['password'] = user.password
	session['first_name'] = user.first_name
	session['last_name'] = user.last_name
	print('SESSION SET')


def grab_props_for_user(user_id):
	results = Reference.query.filter_by(id = user_id).all()
	return results

def decompose_coordinates(coordinates):
	newcoordinates = coordinates.replace('SEPERATOR',',')
	index = 0
	for symbol in newcoordinates:
		index+=1
		if symbol == ",":
			latitude = newcoordinates[0:index-1]
			longitude = newcoordinates[index:len(newcoordinates)]
	return [latitude, longitude]



def grab_home_props():
	properties = []
	random_list= random.sample(range(1, 60), 6)
	for index in range(0,len(random_list)):
		prop = Property.query.filter_by(id=random_list[index]).first()
		print(prop.address)
		properties.append(prop)
	print(properties)
	return properties


def property_current_investment(prop_id):
	reference_obj_list = Reference.query.filter_by(prop_id= prop_id).all()
	total_investment_amount = 0
	if reference_obj_list:
		for reference in reference_obj_list:
			total_investment_amount += reference.investment_value
		return total_investment_amount
	else:
		return total_investment_amount




# ROUTES

@app.route('/', methods=['GET'])
def login_page():
	return render_template('login.html')




@app.route('/onlyforprops', methods=['POST'])
def save_to_db():
	property_list = json.loads(request.data)['result']
	for prop in property_list:
		new_property = Property(
			prop['building_name'],
			datetime.strptime(prop['date_updated'],'%Y-%m-%d').date(),
			prop['coordinates'],
			float(prop['sq_ft']),
			float(prop['bedrooms']),
			float(prop['bathrooms']),
			prop['address'],
			prop['city'],
			prop['state'],
			prop['zipcode'],
			float(int(0)),
			float(int(prop['current_price'])),
			"free"
			)
		print(prop['current_price'])

		db.session.add(new_property)
		db.session.commit()
		print('property added ' + prop['address'])
	print('DONE ADDING PROPERTIES')

	return "Done"


@app.route("/home", methods=['GET', 'POST'])
def home_or_login():
	if request.method == 'GET':
		return render_template('home.html',
			properties = grab_home_props(),
			header = "Random Assortment")
	if request.method == 'POST':
		prov_username = request.form['existUsername']
		prov_password = request.form['existPassword']
		user_result = User.query.filter_by(username=prov_username).first()
		if user_result:
			auth = bcrypt.check_password_hash(user_result.password,prov_password)
			if auth:
				session_set(user_result)
				print(session['username'])
				print(session['user_id'])
				properties = grab_home_props()
				return render_template('home.html',
					properties = properties,
					header = "Random Assortment")
			else:
				return render_template('login.html', 
							lError_message = "Login Credentials were incorrect. Please Try Again."
					)
		else:
			return render_template('login.html', 
							lError_message = "Login Credentials were incorrect. Please Try Again."
					)

@app.route("/register", methods=['GET','POST'])
def register_new_account():
	if request.method=='POST':
		new_username = request.form['newUsername']
		result = User.query.filter_by(username=new_username).first()
		if result:
			return render_template('login.html',

						rError_message="The Username you have provided is already taken.")
		else:
			hashed_password = bcrypt.generate_password_hash(request.form['newPassword']).decode('utf-8')
			new_user = User(new_username,hashed_password,request.form['newFirstName'],request.form['newLastName'],date.today())
			db.session.add(new_user)
			db.session.commit()
			return render_template('login.html',
					lError_message = "Try to log into your new account!"
				)

	if request.method=='GET':
		return render_template('login.html',

						lError_message="Please Login to access content"

			)
	
@app.route('/search', methods=['POST'])
def search():
	search_word = request.form['searchBarInput']
	if "manhattan" in search_word.lower():
		properties = Property.query.filter_by(city = "New York").all()
		print(properties)
		return render_template('home.html',
		properties = properties,
		header="Search Results based on: " + '"'+search_word +'"')
	if "brooklyn" in search_word.lower():
		properties = Property.query.filter_by(city = "Brooklyn").all()
		print(properties)
		return render_template('home.html',
		properties = properties,
		header="Search Results based on: " + '"'+search_word +'"')
	if "jersey" in search_word.lower():
		properties = Property.query.filter_by(city = "Jersey City").all()
		print(properties)
		return render_template('home.html',
		properties = properties,
		header="Search Results based on: " + '"'+search_word +'"')
	else:
		return render_template('home.html',
		properties = grab_home_props(),
		header= '"'+search_word +'"' + " returned nothing. Here is another random assortment!")
	



@app.route("/property/<property_info>", methods=['GET'])
def show_single_property_page(property_info):
	print(property_info)
	result = Property.query.filter_by(id=int(property_info)).first()
	if result:
		check = db.session.query(Reference).filter(Reference.prop_id==result.id, Reference.user_id == session['user_id']).first()
		print(check)
		if check != None:
			print("check route")
			coordinates = decompose_coordinates(result.coordinates)
			investors = grab_other_investors(result.id)
			current_investment_value = property_current_investment(result.id)
			return render_template('singleProperty.html',
				property = result,
				uhoh=uhoh,
				lat = coordinates[0],
				long = coordinates[1],
				check = check,
				investors = investors,
				current_investment_value= current_investment_value)
		else:
			print("nonCheck route")
			coordinates = decompose_coordinates(result.coordinates)
			investors = grab_other_investors(result.id)
			current_investment_value = property_current_investment(result.id)
			return render_template('singleProperty.html',
				property = result,
				uhoh=uhoh,
				lat = coordinates[0],
				long = coordinates[1],
				investors = investors,
				current_investment_value = current_investment_value)
	else:
		return render_template('home.html',
			properties = grab_home_props(),
		)

	
@app.route('/save_property/<key>', methods=['GET'])
def save_property(key):
	new_reference = Reference(session['user_id'],key, 0, 0)	
	db.session.add(new_reference)
	db.session.commit()

	return 


@app.route('/invest_property/<key>', methods=['POST'])
def invest_property(key):
	investment_amount = request.form['investmentAmount']
	new_reference = Reference(session['user_id'],key, 0, investment_amount)	
	db.session.add(new_reference)
	db.session.commit()
	user = User.query.filter_by(id = session['user_id']).first()
	properties = grab_users_properties()
	return render_template('personalPage.html',
		user = user,
		properties = properties
		)


@app.route('/account', methods=["GET","POST"])
def show_account_page():
	if request.method == "GET":
		user = User.query.filter_by(id=session['user_id']).first()
		properties = grab_users_properties()
		return render_template('personalPage.html',
			user = user,
			properties = properties)
	if request.method == "POST":
		new_first_name = request.form['firstNameField']
		print(new_first_name)
		new_last_name = request.form['lastNameField']
		print(new_last_name)
		the_user = User.query.filter_by(id=session['user_id']).first()
		the_user.first_name = new_first_name
		the_user.last_name = new_last_name
		db.session.commit()
		return render_template('login.html',
			lError_message = "To ensure changes have worked, please try to log into your account.")



@app.route('/logout', methods=['GET'])
def logout_return_to_login():
	session.clear()
	return render_template('login.html')


if __name__ == "__main__":
	app.run(debug=True, port=8000)