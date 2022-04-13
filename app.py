
from flask import Flask, jsonify, request, Response, render_template, Blueprint
from flask_pymongo import PyMongo
from bson import json_util
#Importar rutas
from routes.usuarios import usuario
from routes.biblioteca import biblioteca
from routes.prestamos import prestamo

app = Flask(__name__)

#Uso de los imports
app.register_blueprint(usuario)
app.register_blueprint(biblioteca)
app.register_blueprint(prestamo)

#Base de datos
app.config['MONGO_URI'] = 'mongodb://localhost:27017/proyecto2'
#Base de datos en la nube
#app.config['MONGO_URI'] = "mongodb+srv://alvaro:ga1318@cluster0.7pbjf.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
mongo = PyMongo(app)
#db = mongo.db

@app.route("/")
def inicio():
    users = mongo.db.users.find()
    response = json_util.dumps(users)
    return Response(response, mimetype='application/json')


#----------------------ERRORES---------------------------#
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'message': 'Resource Not Found ' + request.url,
        'status': 404
    }
    response = jsonify(message)
    response.status_code = 404
    return response











