# IMPORTS START
from config import DevConfig
from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy



# IMPORTS END


app = Flask(__name__)

app.config.from_object("config.DevConfig")

db = SQLAlchemy(app)



if __name__ == "__main__":
	app.run(debug=True)