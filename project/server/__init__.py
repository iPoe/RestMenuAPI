# project/server/__init__.py
from os import getenv

from dotenv import load_dotenv

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource

from os.path import join, dirname, realpath

UPLOAD_FOLDER = join(dirname(realpath(__file__)), '../../menus_logos_restaurante/')



load_dotenv()


#Cargar las variables de entorno
app = Flask(__name__)
passw = getenv("DB_PASSWORD")
ip = getenv("DB_IP")
dbname = getenv("DB_NAME")
#Url para guardar los datos en gcloud postgres db
DB_URL = "postgres+psycopg2://postgres:{}@{}/{}".format(passw,ip,dbname)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = getenv('SECRET_KEY', 'my_precious')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

api = Api(app)
db = SQLAlchemy(app)

from project.server.restaurant.views import RecursoListarRestaurantes, RecursoUnRestaurante
from project.server.auth.views import RegisterAPI, LoginAPI, LogoutAPI

api.add_resource(RecursoListarRestaurantes,'/restaurantes')
api.add_resource(RecursoUnRestaurante,'/restaurantes/<int:id_restaurante>')

api.add_resource(RegisterAPI,'/registro')
api.add_resource(LoginAPI,'/login')
api.add_resource(LogoutAPI,'/logout')



