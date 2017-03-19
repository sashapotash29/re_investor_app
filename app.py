# IMPORTS START
from config import DevConfig
from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime, date
import json
import random
from models import *



# IMPORTS END


app = Flask(__name__)

app.config.from_object("config.DevConfig")

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)




def grab_home_props():
	properties = []
	random_list= random.sample(range(1, 60), 6)
	for index in range(0,len(random_list)):
		prop = Property.query.filter_by(id=random_list[index]).first()
		print(prop.address)
		properties.append(prop)
	print(properties)
	return properties



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
		return render_template('home.html')
	if request.method == 'POST':
		prov_username = request.form['existUsername']
		prov_password = request.form['existPassword']
		user_result = User.query.filter_by(username=prov_username).first()
		if user_result:
			auth = bcrypt.check_password_hash(user_result.password,prov_password)
			if auth:
				properties = grab_home_props()
				return render_template('home.html',
					properties = properties)
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
	





if __name__ == "__main__":
	app.run(debug=True)