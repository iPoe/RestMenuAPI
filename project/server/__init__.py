# project/server/__init__.py

import os

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource

UPLOAD_FOLDER = '/media/leonardo/HardDisk1/9/Tec Emergentes/TAREA1/RestMenuAPI/menus_logos_restaurantes'



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///restaurantes_jwt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'my_precious')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

api = Api(app)

# PASSWORD ="AHd5MC0Ev964DPna"
# PUBLIC_IP_ADDRESS ="34.66.50.195"
# DBNAME ="restaurantes_jwt"
# PROJECT_ID ="valid-keep-305204"
# INSTANCE_NAME ="api-restaurante"
  
# # configuration 
# #app.config["SECRET_KEY"] = "yoursecretkey"
# app.config["SQLALCHEMY_DATABASE_URI"]= f"mysql + mysqldb://root:{PASSWORD}@{PUBLIC_IP_ADDRESS}/{DBNAME}?unix_socket =/cloudsql/{PROJECT_ID}:{INSTANCE_NAME}"
#app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= True
  
db = SQLAlchemy(app) 



#db = SQLAlchemy(app)


from project.server.restaurant.views import RecursoListarRestaurantes, RecursoUnRestaurante
from project.server.auth.views import RegisterAPI, LoginAPI, LogoutAPI

api.add_resource(RecursoListarRestaurantes,'/restaurantes')
api.add_resource(RecursoUnRestaurante,'/restaurantes/<int:id_restaurante>')

api.add_resource(RegisterAPI,'/registro')
api.add_resource(LoginAPI,'/login')
api.add_resource(LogoutAPI,'/logout')



