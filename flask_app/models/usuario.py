from ..config.mysqlconnection import connectToMySQL
from flask import flash
import re

class Usuario:
    def __init__(self,data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.email = data['email']
        self.password = data['password']
        self.celular = data['celular']
        self.activo = data['activo']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.nivel_usuario_id = data['nivel_usuario_id']

    @classmethod
    def get_por_correo(cls,data):
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        mysql = connectToMySQL('kibo')
        result = mysql.query_db(query, data)
        if len(result) > 0:
            return cls(result[0])
        else:
            return None

    @classmethod
    def get_por_id(cls,id):
        query = "SELECT * FROM usuarios WHERE id = %(id)s;"
        data = {
            "id" : id
        }
        mysql = connectToMySQL('kibo')
        result = mysql.query_db(query, data)
        if len(result) > 0:
            return cls(result[0])
        else:
            return None

    @classmethod
    def get_empleados(cls):
        query = "SELECT * FROM usuarios WHERE nivel_usuario_id = 2;"
        mysql = connectToMySQL('kibo')
        empleados = []
        results = mysql.query_db(query)
        for row in results:
            empleados.append(cls(row))
        return empleados

    @classmethod
    def save(cls,data):
        query = """INSERT INTO usuarios (nombre, apellido, email, password, celular, nivel_usuario_id, activo,
         created_at, updated_at) VALUES (%(nombre)s, %(apellido)s, %(email)s, %(password)s, %(celular)s, %(nivel_usuario_id)s, 1,
         NOW(), NOW());"""
        return connectToMySQL('kibo').query_db(query,data)

    @classmethod
    def update(cls, data ):
        if("password" in data):
            query = """UPDATE usuarios SET nombre = %(nombre)s , apellido = %(apellido)s , email = %(email)s, 
            password = %(password)s, celular = %(celular)s, updated_at = NOW() WHERE id = %(id)s;"""
        else:
            query = """UPDATE usuarios SET nombre = %(nombre)s , apellido = %(apellido)s, email = %(email)s, 
            celular = %(celular)s, updated_at = NOW() WHERE id = %(id)s;"""
        return connectToMySQL('kibo').query_db( query, data)
    
    @classmethod
    def update_estado(cls, data ):
        if(data["estado"] == "1"):
            query = "UPDATE usuarios SET activo = 0 WHERE id = %(id)s"
        else:
            query = "UPDATE usuarios SET activo = 1 WHERE id = %(id)s"
        return connectToMySQL('kibo').query_db( query, data)


    @staticmethod
    def validar_registro(datos):
        is_valid = True
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        data = {
            "email" : datos["email"]
        }
        results = connectToMySQL('kibo').query_db(query,data)
        if len(results) >= 1:
            flash("El email ya está registrado.", "usuario")
            is_valid = False
        
        return is_valid

    @staticmethod
    def obtener_nombre(id):
        query = f"SELECT nombre, apellido FROM usuarios WHERE id = {id};"
        mysql = connectToMySQL('kibo')
        result = mysql.query_db(query)
        if len(result) > 0:
            return result[0]['nombre'] + " " +result[0]['apellido']
        else:
            return "Nombre no encontrado"


