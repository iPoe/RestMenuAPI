# project/server/__init__.py

import os

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///restaurantes_jwt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'my_precious')

api = Api(app)

db = SQLAlchemy(app)


from project.server.restaurant.views import RecursoListarRestaurantes, RecursoUnRestaurante
from project.server.auth.views import RegisterAPI, LoginAPI, LogoutAPI

api.add_resource(RecursoListarRestaurantes,'/restaurantes')
api.add_resource(RecursoUnRestaurante,'/restaurantes/<int:id_restaurante>')

api.add_resource(RegisterAPI,'/registro')
api.add_resource(LoginAPI,'/login')
api.add_resource(LogoutAPI,'/logout')



