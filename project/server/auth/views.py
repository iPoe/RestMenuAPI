# project/server/auth/views.py

from flask import request, make_response, jsonify
from flask.views import MethodView

from project.server import db, api
from project.server.models import User, BlacklistToken
from flask_restful import Resource


def get_token():
    # get auth token
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = ''
    return auth_token


class RegisterAPI(Resource):
    """
    User Registration Resource
    """

    def post(self):
        # get the post data
        post_data = request.get_json()
        # check if user already exists
        user = User.query.filter_by(email=post_data.get('email')).first()
        if not user:
            try:
                user = User(
                    email=post_data.get('email'),
                    password=post_data.get('password')
                )

                # insert the user
                db.session.add(user)
                db.session.commit()
                # generate the auth token
                auth_token = user.encode_auth_token(user.id)
                responseObject = {
                    'status': 'exito',
                    'message': 'Registro exitoso',
                    'auth_token': auth_token.decode()
                }
                return make_response(jsonify(responseObject))
            except Exception as e:
                responseObject = {
                    'status': 'Error',
                    'message': 'Algo ocurrio, intenta de nuevo'
                }
                return make_response(jsonify(responseObject))
        else:
            responseObject = {
                'status': 'Error',
                'message': 'Usuario ya registrado. Inicie Sesion',
            }
            return make_response(jsonify(responseObject))

class LoginAPI(Resource):
    """
    User Login Resource
    """
    def post(self):
        # get the post data
        post_data = request.get_json()
        try:
            # fetch the user data
            user = User.query.filter_by(
                email=post_data.get('email')
            ).first()
            if user and user.password == post_data.get('password'):
                auth_token = user.encode_auth_token(user.id)
                if auth_token:
                    responseObject = {
                        'status': 'exito',
                        'message': 'Inicio de sesion exitoso',
                        'auth_token': auth_token.decode()
                    }
                    return make_response(jsonify(responseObject))
            else:
                responseObject = {
                    'status': 'Error',
                    'message': 'Usuario inexistente'
                }
                return make_response(jsonify(responseObject))
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'Error',
                'message': 'Intente de Nuevo'
            }
            return make_response(jsonify(responseObject))

class LogoutAPI(Resource):
    """
    Logout Resource
    """
    def post(self):
        auth_token = get_token()
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                # mark the token as blacklisted
                blacklist_token = BlacklistToken(token=auth_token)
                try:
                    # insert the token
                    db.session.add(blacklist_token)
                    db.session.commit()
                    responseObject = {
                        'status': 'exito',
                        'message': 'Cierre de sesion exitoso'
                    }
                    return make_response(jsonify(responseObject))
                except Exception as e:
                    responseObject = {
                        'status': 'Error',
                        'message': e
                    }
                    return make_response(jsonify(responseObject))
            else:
                responseObject = {
                    'status': 'Error',
                    'message': resp
                }
                return make_response(jsonify(responseObject))
        else:
            responseObject = {
                'status': 'Error',
                'message': 'Token invalido'
            }
            return make_response(jsonify(responseObject))



