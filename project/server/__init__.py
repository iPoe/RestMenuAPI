# project/server/__init__.py

import os

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import sqlalchemy
#...

# load dotenv in the base root
APP_ROOT = os.path.join(os.path.dirname(__file__), '..')   # refers to application_top
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)
UPLOAD_FOLDER = '/media/leonardo/HardDisk1/9/Tec Emergentes/TAREA1/RestMenuAPI/menus_logos_restaurantes'



app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///restaurantes_jwt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'my_precious')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

api = Api(app)

engine = create_engine('postgresql+psycopg2://restaurantes_jwt:Monster14320@localhost:5432/')
conn = engine.connect()
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

  
#db = SQLAlchemy(app)



from project.server.restaurant.views import RecursoListarRestaurantes, RecursoUnRestaurante
from project.server.auth.views import RegisterAPI, LoginAPI, LogoutAPI

api.add_resource(RecursoListarRestaurantes,'/restaurantes')
api.add_resource(RecursoUnRestaurante,'/restaurantes/<int:id_restaurante>')

api.add_resource(RegisterAPI,'/registro')
api.add_resource(LoginAPI,'/login')
api.add_resource(LogoutAPI,'/logout')



