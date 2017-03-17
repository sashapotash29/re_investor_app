# IMPORTS START
from config import DevConfig
from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
import json
from models import *



# IMPORTS END


app = Flask(__name__)

app.config.from_object("config.DevConfig")

db = SQLAlchemy(app)



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


if __name__ == "__main__":
	app.run(debug=True)