from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def initialize_db(app):
	app.logger.info("Initializing MySQL")
	db.init_app(app)