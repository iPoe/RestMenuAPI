# project/server/models.py

import datetime

from project.server import app, db, api
import jwt

class User(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    relation = db.relationship('Restaurante', backref='user', lazy=True)

    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=0),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Validates the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'No existe una sesion abierta'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Token Invalido. Inicia sesion de Nuevo'


class BlacklistToken(db.Model):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    @staticmethod
    def check_blacklist(auth_token):
        # check whether auth token has been blacklisted
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True  
        else:
            return False

class Restaurante(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    nombre = db.Column(db.String(50), nullable=False)
    lugar = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(50), nullable=False) #revisar
    direccion = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.Integer, nullable=False)
    logo_rest = db.Column(db.String(100), nullable=False)
    menu = db.Column(db.String(100), nullable=False)
    domicilio = db.Column(db.Boolean, nullable=False)
    #fecha_creacion = db.Column(db.DateTime, nullable=False) revisar

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)



