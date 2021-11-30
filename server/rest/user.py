from flask import Response, request
from flask import current_app as app
from db.models import User
from flask_restful import Resource
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import exc
from errors import InternalServerError, SchemaValidationError, UserNotFoundError, EmailAlreadyExistError
from datetime import date, datetime
from db.models import db
from faker import Faker
from faker.providers import date_time
import json

fake = Faker()
fake.add_provider(date_time)

class UsersApi(Resource):
	def get(self):
		users = User.query.all()
		users_to_send = json.dumps([user.serialize() for user in users])
		#app.logger.info(users_to_send)
		return Response(users_to_send, mimetype="application/json", status=200)

	def delete(self):
		user = User.objects.delete()
		return '', 200

	def post(self):
		try:
			#body = json.loads(request.get_json())
			body = {}
			body['birthdate'] = fake.date()
			body["name"] = fake.name()
			body["email"] = fake.email()

			#app.logger.info(body)
			#user = User(name=body["name"], email=body["email"], birthdate=datetime.strptime(body["birthdate"], '%Y-%m-%d').date())
			user = User(name=body["name"], email=body["email"], birthdate=body["birthdate"])
			
			db.session.add(user)
			db.session.commit()
			#app.logger.info(user.serialize())
			id = user.id
			return {'id': str(id)}, 201
		except exc.IntegrityError:
			raise EmailAlreadyExistError
		except Exception as e:
			app.logger.error(e)
			raise InternalServerError

class UserApi(Resource):
	def put(self, id):
		body = request.get_json()
		User.objects.get(id=id).update(**body)
		return '', 200

	def get(self, id):
		try:
			users = User.objects.get(id=id).to_json()
			return Response(users, mimetype="application/json", status=200)
		except NoResultFound:
			raise UserNotFoundError

	def delete(self, id):
		user = User.objects.get(id=id).delete()
		return '', 200