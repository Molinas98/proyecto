from ..config.mysqlconnection import connectToMySQL
from flask import flash
from . import usuario
from datetime import datetime
import re

class Trabajo:
    def __init__(self,data):
        self.id = data['id']
        self.titulo = data['titulo']
        self.descripcion = data['descripcion']
        self.tipo = data['tipo']
        self.fecha_limite = data['fecha_limite']
        self.foto_detalles = data['foto_detalles']
        self.documento = data['documento']
        self.precio = data['precio']
        self.comentario = data['comentario']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.usuario_id = data['usuario_id']
        self.estado_id = data['estado_id']
        self.estado_anterior_id = data['estado_anterior_id']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM trabajos;"
        trabajos = []
        results = connectToMySQL('kibo').query_db(query)
        for row in results:
            trabajos.append(cls(row))
        return trabajos
    
    @classmethod
    def get_all_user(cls, id):
        query = "SELECT * FROM trabajos WHERE usuario_id = %(usuario_id)s;"
        data = {
            "usuario_id" : id
        }
        results = connectToMySQL('kibo').query_db(query, data)
        trabajos = []
        for row in results:
            trabajos.append(cls(row))
        return trabajos
    
    @classmethod
    def get_estados(cls, id, nivel):
        query = """SELECT trabajos.id, titulo, anterior.estado AS anterior, actual.estado AS actual from trabajos LEFT JOIN estados anterior ON 
        trabajos.estado_anterior_id = anterior.id LEFT JOIN estados actual ON trabajos.estado_id = actual.id LEFT JOIN trabajos_asignados
        ON trabajos_asignados.trabajo_id = trabajos.id WHERE (trabajos_asignados.empleado_id = %(id)s OR trabajos.usuario_id = %(id)s);"""
        data = {
            "id" : id
        }
        results = connectToMySQL('kibo').query_db(query,data)
        estados = []
        if nivel == 1 or nivel == 2:
            notificaciones_aceptadas = [['Aceptado','En Proceso'], ['Esperando Pago','Pago a confirmar'], ['Finalizado','Entregado'], ['Aceptado','Rechazado'], ['Enviado','Cancelado']]
        else:
            notificaciones_aceptadas = [['Enviado','Aceptado'], ['En Proceso','Esperando Pago'], ['En Proceso','Finalizado'], ['Esperando Pago','Finalizado'], ['Pago a confirmar','Finalizado'], ['Enviado','Rechazado']]
        for row in results:
            if([row['anterior'], row['actual']] in notificaciones_aceptadas):
                estados.append(row)
        return estados
    


    @classmethod
    def get_one(cls,id):
        query = "SELECT * FROM trabajos WHERE id = %(id)s;"
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
    def save(cls,data):
        query = """INSERT INTO trabajos (titulo, descripcion, tipo, fecha_limite, foto_detalles, estado_id, estado_anterior_id,
         created_at, updated_at, usuario_id) VALUES (%(titulo)s, %(descripcion)s, %(tipo)s, %(fecha_limite)s, %(foto_detalles)s,
         1, 1, NOW(), NOW(), %(usuario_id)s);"""
        return connectToMySQL('kibo').query_db(query,data)
        
    @classmethod
    def update(cls, data):
        query = "UPDATE trabajos SET estado_id = %(estado)s, estado_anterior_id = (SELECT estado_id FROM trabajos WHERE id = %(id)s) WHERE id = %(id)s;"
        return connectToMySQL('kibo').query_db( query, data)
    
    @classmethod
    def complete(cls, data):
        query = "UPDATE trabajos SET precio = %(precio)s, comentario = %(comentario)s, estado_id = %(estado)s, estado_anterior_id = (SELECT estado_id FROM trabajos WHERE id = %(id)s)  WHERE id = %(id)s;"
        return connectToMySQL('kibo').query_db( query, data)
    
    @classmethod
    def send(cls, data):
        query = "UPDATE trabajos SET documento = %(documento)s , estado_id = %(estado)s, estado_anterior_id = (SELECT estado_id FROM trabajos WHERE id = %(id)s)  WHERE id = %(id)s;"
        return connectToMySQL('kibo').query_db( query, data)
    
    @classmethod
    def igualar_estado(cls, id):
        query = "UPDATE trabajos SET estado_anterior_id = estado_id  WHERE id = %(id)s;"
        data = {
            "id" : id
        }
        return connectToMySQL('kibo').query_db( query, data)


    @staticmethod
    def obtener_estado(id):
        query = f"SELECT estado FROM estados WHERE id = {id};"
        mysql = connectToMySQL('kibo')
        result = mysql.query_db(query)
        if len(result) > 0:
            return result[0]['estado']
        else:
            return "Estado indeterminado"
        
    @staticmethod
    def obtener_ultimo_id():
        query = "SELECT MAX(id) as ultimo FROM trabajos;"
        mysql = connectToMySQL('kibo')
        result = mysql.query_db(query)
        if result[0]["ultimo"] != None:
            return result[0]['ultimo'] + 1
        else:
            return 1

    @staticmethod
    def validate_precio(datos):
        is_valid = True # asumimos que esto es true
        if len(datos) < 4:
            flash("Define un precio para trabajo")
            is_valid = False
        
        return is_valid

