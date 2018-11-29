from app import db, bcrypt, app, ma
import datetime
import jwt
from flask_validator import ValidateInteger, ValidateString, ValidateEmail

class User( db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(255), nullable=False)
	password = db.Column(db.String(255), nullable=False)
	username = db.Column(db.String(120), unique=True, nullable=False)
	email = db.Column(db.String(255), unique=True, nullable=False)
	email_verified_at = db.Column(db.TIMESTAMP(), nullable=True)
	remember_token = db.Column(db.String(120), nullable=True)
	created_at = db.Column(db.TIMESTAMP(), nullable=True, server_default=db.func.now())
	updated_at = db.Column(db.TIMESTAMP(), nullable=True, server_default=db.func.now(), server_onupdate=db.func.now())

	def __init__(self,name, email,username, password):
		self.name = name
		self.email = email
		self.username = username
		self.password = bcrypt.generate_password_hash(password, 10)

	# @classmethod
	# def __declare_last__(cls):
	# 	ValidateString(User.name)
	# 	ValidateEmail(User.email, True, True, "The e-mail is not valid. Please check it")

	#genarate hash pasword
	def generatePasswordHash(password):
		return bcrypt.generate_password_hash(password, 10)
	def verifyPassword(self, password):
		return bcrypt.check_password_hash(self.password, password)
	# funtion 
	def delete(self):
		db.session.delete(self)
		db.session.commit()

	#JWT
	def encodeAuthToken(self, user_id):
		"""
		Generates the Auth Token
	    :return: string
		"""
		try:
			payload = {
				'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=36000),
	            'iat': datetime.datetime.utcnow(),
	            'user_id': user_id
			}
			return jwt.encode(
				payload,
				app.config.get('SECRET_KEY'),
				algorithm='HS256'
			)
		except Exception as e:
			return e
	#decode auth token
	@staticmethod
	def decodeAuthToken(auth_token):
		"""
		Decodes the auth token
		:param auth_token:
		:return: integer|string
		"""
		try:
			payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
			return payload['user_id']
		except jwt.ExpiredSignatureError:
			return 'Signature expired. Please log in again.'
		except jwt.InvalidTokenError:
			return 'Invalid token. Please log in again.'

#Tạo Schema cho model
class UserSchema(ma.ModelSchema):
	class Meta:
		fields = ('id','username','email', 'created_at', 'updated_at')

user_schema = UserSchema()