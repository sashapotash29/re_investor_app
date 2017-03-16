class Config:
	SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/realvest.db'
	SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
	DEBUG = True


class ProdConfig(Config):
	DEBUG = False
	ALLOWED_HOSTS = ["*"]