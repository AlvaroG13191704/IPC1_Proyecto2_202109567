#imports
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, Response
from bson import json_util
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
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
    #
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

#Login
@usuario.route("/user_login", methods = ['POST'])
def login():
    #Iniciar mongo
    mongo = PyMongo(app.app)
    #Hacer el login
    user_nickname = request.json['user_nickname']
    user_password = request.json['user_password']
    #Verificar que el usuario exista
    if mongo.db.users.find_one({"user_nickname": user_nickname}):
        #Verificar que la contraseña sea correcta
        if mongo.db.users.find_one({"user_nickname": user_nickname, "user_password": user_password}):
            user = mongo.db.users.find_one({"user_nickname": user_nickname, "user_password": user_password})
            response = json_util.dumps(user)
            return Response(response, mimetype='application/json'), 200
        else:
            return jsonify({'msg': 'Contraseña incorrecta'}), 400
    return jsonify({'msg': 'Usuario no registrado'}), 400
#--------------------ENDLOGIN------------------------------#  