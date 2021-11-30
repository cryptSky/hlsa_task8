import json

from flask import Flask
from flask_cors import CORS

from config import BaseConfig
from db import initialize_db
from rest import initialize_api

from logging.config import dictConfig
import pymysql

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'formatter': 'default'
    }},
    'root': {
        'level': 'DEBUG',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)
CORS(app)
app.config.from_object(BaseConfig)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:password@db/db'

initialize_db(app)

initialize_api(app)


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=8000)