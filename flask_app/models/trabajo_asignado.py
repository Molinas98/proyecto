from ..config.mysqlconnection import connectToMySQL
from flask import flash
import re
from ..models import trabajo

class Trabajo_asignado:
    def __init__(self,data):
        self.id = data['id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.trabajo_id = data['trabajo_id']
        self.empleado_id = data['empleado_id']
        self.trabajo = None

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM trabajos_asignados LEFT JOIN trabajos ON trabajos_asignados.trabajo_id = trabajos.id;"
        mysql = connectToMySQL('kibo')
        trabajos = []
        results = mysql.query_db(query)
        for row in results:
            trabajo_asignado = cls(row)
            trabajo_datos = {
                "id" : row["trabajos.id"],
                "titulo" : row["titulo"],
                "descripcion" : row["descripcion"],
                "tipo" : row["tipo"],
                "fecha_limite" : row["fecha_limite"],
                "foto_detalles" : row["foto_detalles"],
                "documento" : row["documento"],
                "precio" : row["precio"],
                "comentario" : row["comentario"],
                "created_at" : row["trabajos.created_at"],
                "updated_at" : row["trabajos.updated_at"],
                "usuario_id" : row["usuario_id"],
                "estado_id" : row["estado_id"],
                "estado_anterior_id" : row["estado_anterior_id"]
            }
            trabajo_asignado.trabajo = trabajo.Trabajo(trabajo_datos)
            trabajos.append(trabajo_asignado)
        return trabajos

    @classmethod
    def save(cls,data):
        query = """INSERT INTO trabajos_asignados (trabajo_id, empleado_id, created_at, updated_at) VALUES 
        (%(trabajo_id)s, %(empleado_id)s,NOW(), NOW());"""
        return connectToMySQL('kibo').query_db(query,data)



