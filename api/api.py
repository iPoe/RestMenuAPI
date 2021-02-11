import flask
from flask import request, jsonify


app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Api de restaurantes</h1><p>Bienvenido a nuestra API de restaurantes.</p>"


@app.route('/login',methods=['GET','POST'])
def login_usuario():
    data = request.json
    # if request.method == 'POST':
    #     request
    # else:
    #     return "El campo de correo no puede ser vacio"
    
    return jsonify("Bienvenido "+data['idusuario'])

@app.route('/addres', methods=['GET'])
def agregar_restaurante():
    #Sentencias o Querys que agregan el restaurante en BD
    return "Restaurante agregado"

app.run()