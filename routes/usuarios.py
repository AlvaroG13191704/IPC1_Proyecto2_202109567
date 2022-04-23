#imports
from flask import Blueprint, request, jsonify, Response
from bson import json_util
from flask_pymongo import PyMongo
import app
usuario=Blueprint("usuarios",__name__)

#--------------------LOGIN------------------------------#
#Registrar user
@usuario.route("/user", methods = ['POST'])
def register_user(): 
    #Recibir y guardar datos en la base de datos
    id_user = request.json['id_user']
    user_display_name = request.json['user_display_name']
    user_nickname = request.json['user_nickname']
    user_password = request.json['user_password']
    user_age = request.json['user_age']
    user_career = request.json['user_career']
    user_carnet = request.json['user_carnet']
    #Verificar que id_user no este repetido
    #Iinciar mongo
    mongo = PyMongo(app.app)  
    if id_user and user_display_name and user_nickname and user_password and user_age and user_career and user_carnet:
        if mongo.db.users.find_one({"id_user": id_user}):
            return jsonify({'msg': 'El id_user ya existe'}), 400
        else:
            mongo.db.users.insert_one({
                "id_user": id_user,
                "user_display_name": user_display_name,
                "user_nickname": user_nickname,
                "user_password": user_password,
                "user_age": user_age,
                "user_career": user_career,
                "user_carnet": user_carnet
            })
        response = jsonify({"status": 200, "msg": "response"})
        response.status_code = 200
        return response
    else:
        response = jsonify({"status": 400, "msg": "Datos insuficientes"})
        response.status_code = 400
        return response 

#Login
@usuario.route("/user_login", methods = ['POST'])
def login():
    #Iniciar mongo
    mongo = PyMongo(app.app)
    #Hacer el login
    user_nickname = request.json['user_nickname']
    user_password = request.json['user_password']
    #Verificar que el usuario exista
    if user_nickname and user_password:
        if mongo.db.users.find_one({"user_nickname": user_nickname}):
            #Verificar que la contraseña sea correcta
            if mongo.db.users.find_one({"user_nickname": user_nickname, "user_password": user_password}):
                user = mongo.db.users.find_one({"user_nickname": user_nickname, "user_password": user_password})
                response = json_util.dumps(user)
                return Response(response, mimetype='application/json'), 200
            else:
                return jsonify({'msg': 'Contraseña incorrecta'}), 400
        return jsonify({'msg': 'Usuario no registrado'}), 400
    else: 
        response = jsonify({"status": 400, "msg": "Datos insuficientes"})
        response.status_code = 400
        return response
#--------------------ENDLOGIN------------------------------#  
@usuario.route('/user_update', methods = ['GET','POST'])
def update():
    #Iniciar mongo
    mongo = PyMongo(app.app)
    #Recibir datos
    id_user = request.json['id_user']
    user_display_name = request.json['user_display_name']
    user_nickname = request.json['user_nickname']
    user_password = request.json['user_password']
    user_age = request.json['user_age']
    user_career = request.json['user_career']
    user_carnet = request.json['user_carnet']
    #Verificar que el id exista pra hacer la actualizacion
    if mongo.db.users.find_one({"id_user":id_user}):
        #Actualizar los datos
        mongo.db.users.update_one({"id_user":id_user}, {
            '$set':{
                "id_user": id_user,
                "user_display_name": user_display_name,
                "user_nickname": user_nickname,
                "user_password": user_password,
                "user_age": user_age,
                "user_career": user_career,
                "user_carnet": user_carnet
            }
        })
        user = mongo.db.users.find_one({"id_user": id_user})
        response = json_util.dumps(user)
        return Response(response, mimetype='application/json'), 200 
    else:
        return jsonify({'msg': 'Usuario no registrado'}), 400

"""
Terminado-----<>
agregar usuarios JSON model
{
    "id_user": "oasdoe2s",
    "user_display_name" : "Alvaro Norberto García Meza",
    "user_nickname": "AlvaroG1318",
    "user_password": "ga1318",
    "user_age": 18,
    "user_career": "Ingenieria en Ciencias y Sistemas",
    "user_carnet": 202109567
}
Para Logearse
{
    "user_nickname":"AlvaroG1318",
    "user_password":"ga1318"
}
"""