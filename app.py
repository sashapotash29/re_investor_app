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



	# # SCHEMA
	# id = db.Column(db.Integer, primary_key=True)
	# building_name = db.Column(db.String(40), primary_key=True)
	# date_updated = db.Column(db.Date)
	# sq_ft = db.Column(db.Float, primary_key=True)
	# bedrooms = db.Column(db.Float, primary_key=True)
	# bathrooms = db.Column(db.Float, primary_key=True)
	# address = db.Column(db.String(100))
	# city = db.Column(db.String(30))
	# state = db.Column(db.String(20))
	# zipcode = db.Column(db.String(30))
	# past_price = db.Column(db.Float)
	# current_price = db.Column(db.Float)
	# status = db.Column(db.String)








if __name__ == "__main__":
	app.run(debug=True)