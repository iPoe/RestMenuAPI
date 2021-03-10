# project/server/restaurant/views.py

from flask import request, make_response, jsonify
from flask.views import MethodView

from project.server import db, api, app
from project.server.models import Restaurante, User, BlacklistToken
from flask_restful import Resource
import jwt
import os
from flask_marshmallow import Marshmallow
from sqlalchemy import desc
import base64

from google.cloud import storage
from os.path import join, dirname, realpath

ma = Marshmallow(app)


def push_to_bucket(source_file_name,destination_blob_name):
    client = storage.Client.from_service_account_json("api-menu-key.json")
    bucket = client.get_bucket('rest-menus')
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)    


class Restaurante_Schema(ma.Schema):
    class Meta:
        fields = ("id","nombre","lugar","categoria","direccion","telefono","logo_rest","menu","domicilio","user_id")

post_schema = Restaurante_Schema() #Un solo restaurante
posts_schema = Restaurante_Schema(many = True) # varios restaurantes

def get_token(auth_header):
    # get auth token
    ans = False
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = ''
    if auth_token:
        resp = User.decode_auth_token(auth_token)
        if not isinstance(resp, str):
            ans = True
    return ans


class RecursoListarRestaurantes(Resource):
    
    def get(self):
        auth_header = request.headers.get('Authorization')
        auth_token = get_token(auth_header)
        if auth_token:
            token = auth_header.split(" ")[1]
            payload = jwt.decode(token, app.config.get('SECRET_KEY'))
            restaurantes = Restaurante.query.filter_by(user_id=payload['sub']).order_by(desc(Restaurante.id))
            return posts_schema.dump(restaurantes)
        else:
            responseObject = {
                'status': 'Error',
                'message': 'acceso denegado!, inicia sesion para adquirir permisos'
            }
            return make_response(jsonify(responseObject))

    def post(self):
        auth_header = request.headers.get('Authorization')
        auth_token = get_token(auth_header)
        if auth_token:
            token = auth_header.split(" ")[1]
            payload = jwt.decode(token, app.config.get('SECRET_KEY'))
            logo_r = request.files['logo_rest']
            logo_r.save(os.path.join(app.config['UPLOAD_FOLDER'], logo_r.filename))
            logo_m = request.files['menu']
            logo_m.save(os.path.join(app.config['UPLOAD_FOLDER'], logo_m.filename))
            #Guardar el menu en el bucket
            push_to_bucket(app.config['UPLOAD_FOLDER']+logo_m.filename,logo_m.filename)
            push_to_bucket(app.config['UPLOAD_FOLDER']+logo_r.filename,logo_r.filename)

            nuevo_restaurante = Restaurante(
                nombre = request.form['nombre'],
                lugar = request.form['lugar'],
                categoria = request.form['categoria'],
                direccion = request.form['direccion'],
                telefono = request.form['telefono'],
                logo_rest = logo_r.filename,
                menu = logo_m.filename,
                domicilio = request.form['domicilio'],
                user_id = payload['sub']
            )
          
            db.session.add(nuevo_restaurante)
          
            db.session.commit()
           
            return post_schema.dump(nuevo_restaurante)
        else:
            responseObject = {
                'status': 'Error',
                'message': 'acceso denegado!, inicia sesion para adquirir permisos'
            }
            return make_response(jsonify(responseObject))

class RecursoUnRestaurante(Resource):
    
    def get(self, id_restaurante):
        auth_header = request.headers.get('Authorization')
        auth_token = get_token(auth_header)
        if auth_token:
            restaurante = Restaurante.query.get_or_404(id_restaurante)
            return post_schema.dump(restaurante)
        else:
            responseObject = {
                'status': 'Error',
                'message': 'acceso denegado!, inicia sesion para adquirir permisos'
            }
            return make_response(jsonify(responseObject))

        

    def put(self, id_restaurante):
        auth_header = request.headers.get('Authorization')
        auth_token = get_token(auth_header)
        if auth_token:

            restaurante = Restaurante.query.get_or_404(id_restaurante)
            if 'nombre' in request.form:
                restaurante.nombre = request.form['nombre']
            if 'lugar' in request.form:
                restaurante.lugar = request.form['lugar']
            if 'categoria' in request.form:
                restaurante.categoria = request.form['categoria']
            if 'direccion' in request.form:
                restaurante.direccion = request.form['direccion']
            if 'telefono' in request.form:
                restaurante.telefono = request.form['telefono']
            if 'logo_rest' in request.files:

                logo_r = request.files['logo_rest']
                logo_r.save(os.path.join(app.config['UPLOAD_FOLDER'], logo_r.filename))
                restaurante.logo_rest = logo_r.filename

            if 'menu' in request.files:

                logo_m = request.files['menu']
                logo_m.save(os.path.join(app.config['UPLOAD_FOLDER'], logo_m.filename))
                restaurante.menu = logo_m.filename

            if 'domicilio' in request.form:
                restaurante.domicilio = request.form['domicilio']

            
            db.session.commit()
            return post_schema.dump(restaurante)
        else:
            responseObject = {
                'status': 'Error',
                'message': 'acceso denegado!, inicia sesion para adquirir permisos'
            }
            return make_response(jsonify(responseObject))

    def delete(self, id_restaurante):
        auth_header = request.headers.get('Authorization')
        auth_token = get_token(auth_header)
        if auth_token:

            restaurante = Restaurante.query.get_or_404(id_restaurante)
            db.session.delete(restaurante)
            db.session.commit()
            return 'Eliminacion Exitosa'
        else:
            responseObject = {
                'status': 'Error',
                'message': 'acceso denegado!, inicia sesion para adquirir permisos'
            }
            return make_response(jsonify(responseObject))
        



