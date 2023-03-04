from flask_app import app
from flask import render_template, request, redirect, session, flash, jsonify 
from werkzeug.utils import secure_filename 
import os
from ..models.usuario import Usuario
from ..models.trabajo import Trabajo
from ..models.trabajo_asignado import Trabajo_asignado


@app.route('/trabajo/<int:id>', methods=['GET'])
def mostrar_trabajo(id):
    if session.get('id') == None:
        return redirect('/')
    else:
        session["update"] = "no"
        usuario = Usuario.get_por_id(session['id'])
        trabajo = Trabajo.get_one(id)
        if usuario.nivel_usuario_id <= 2:
            if trabajo.estado_id == 7 or trabajo.estado_id == 8:
                return render_template('trabajo_enviado.html', usuario = usuario, trabajo = trabajo)
            else:
                return render_template('trabajo_admin.html', usuario = usuario, trabajo = trabajo)
        else:
            if trabajo.estado_id == 1 or trabajo.estado_id == 7 or trabajo.estado_id == 8:
                return render_template('trabajo_enviado.html', usuario = usuario, trabajo = trabajo)
            elif trabajo.estado_id == 2 or trabajo.estado_id == 3 or trabajo.estado_id == 9:
                return render_template('trabajo_cliente.html', usuario = usuario, trabajo = trabajo)
            elif trabajo.estado_id == 4 or trabajo.estado_id == 5:
                return render_template('cliente_trabajo_notificacion.html', usuario = usuario, trabajo = trabajo)
            elif trabajo.estado_id == 6:
                #el estado del trabajo pasa a entregado cuando se abre el link
                data = {
                    "id" : id,
                    "estado" : 9
                }
                Trabajo.update(data)
                return render_template('cliente_trabajo_terminado.html', usuario = usuario, trabajo = trabajo)
            else:
                return redirect("/dashboard")

@app.route("/process_notificaciones")
def obtener_estados():
    usuario = Usuario.get_por_id(session["id"])
    estados = Trabajo.get_estados(usuario.id, usuario.nivel_usuario_id)
    return jsonify(estados)

@app.route("/actualizar_estados/<int:id>")
def actualizar_estados(id):
    Trabajo.igualar_estado(id)
    return jsonify(message ="exito")

@app.route('/dashboard/process', methods=['GET', 'POST'])
def solicitar_trabajo():
    if request.method == 'POST':
        path_database = None
        if request.files["foto_detalles"].filename != "":
            EXTENSIONES_PERMITIDAS = set([".png", ".jpg", ".jpeg"])
            file     = request.files['foto_detalles']
            basepath = os.path.dirname (__file__) #La ruta donde se encuentra el archivo actual
            #dividimos los diferentes carpetas
            carpetas = basepath.split("\\")
            #Al url base que termina en controllers le sustraemos la misma para retroceder una carpeta
            #Para eso tomamos en cuenta la longitud de la ultima carpeta y le restamos tambien el caracter de la barra inclinada
            basepath = basepath[:(len(basepath)-len(carpetas[len(carpetas)-1])-1)]
            filename = secure_filename(file.filename) #Nombre original del archivo
            
            #capturando extension del archivo ejemplo: (.png, .jpg)
            extension           = os.path.splitext(filename)[1]
            #validando la extension
            if not extension in EXTENSIONES_PERMITIDAS:
                return jsonify(mensaje ="Imagen no válida, las extensiones permitidas son .png, .jpg, .jpeg")

            nuevoNombreFile     = str(Trabajo.obtener_ultimo_id()) + extension
            upload_path = os.path.join (basepath, 'static\\files', nuevoNombreFile) 
            file.save(upload_path)
            path_database = f"/static/files/{nuevoNombreFile}"

        data = {
            "titulo": request.form["titulo"],
            "descripcion": request.form["descripcion"],
            "tipo": request.form["tipo"],
            "fecha_limite": request.form["fecha_limite"],
            "foto_detalles": path_database,
            "usuario_id": session["id"]
        }
        Trabajo.save(data)
        return redirect('/dashboard')
    else:
        return redirect('/dashboard')


@app.route('/trabajo/update/' , methods=['GET', 'POST'])
def actualizar_estado():
    if request.method == 'POST':
        data = {
            "id" : request.form["id"],
            "estado" : request.form["proximo_estado"]
        }
        Trabajo.update(data)
        return redirect('/dashboard')
    else:
        return redirect('/dashboard')
    
@app.route('/trabajo/complete/' , methods=['GET', 'POST'])
def completar_trabajo():
    if request.method == 'POST':
        if not Trabajo.validate_precio(request.form["precio"]):
            return redirect("/trabajo/" + str(request.form["id"]))
        data = {
            "id" : request.form["id"],
            "precio": request.form["precio"],
            "comentario": request.form["comentario"],
            "estado" : request.form["proximo_estado"]
        }
        Trabajo.complete(data)
        data2 = {
            "trabajo_id" : request.form["id"],
            "empleado_id" : session['id']
        }
        Trabajo_asignado.save(data2)
        return redirect('/dashboard')
    else:
        return redirect('/dashboard')
    
@app.route('/trabajo/send/' , methods=['GET', 'POST'])
def enviar_trabajo():
    if request.method == 'POST':
        if request.files["trabajo_terminado"].filename == "":
            flash("Sube archivo del trabajo finalizado")
            return redirect("/trabajo/" + str(request.form["id"]))
        file = request.files['trabajo_terminado']
        basepath = os.path.dirname (__file__) #La ruta donde se encuentra el archivo actual
        print("HOLLAAA")
        print(type(basepath))
        #dividimos los diferentes carpetas
        carpetas = basepath.split("\\")
        #Al url base que termina en controllers le sustraemos la misma para retroceder una carpeta
        #Para eso tomamos en cuenta la longitud de la ultima carpeta y le restamos tambien el caracter de la barra inclinada
        basepath = basepath[:(len(basepath)-len(carpetas[len(carpetas)-1])-1)]
        filename = secure_filename(file.filename) #Nombre original del archivo
        #capturando extension del archivo ejemplo: (.png, .jpg)
        extension = os.path.splitext(filename)[1]

        nuevoNombreFile     = "trabajo_" + str(request.form["id"]) + extension
        upload_path = os.path.join (basepath, 'static\\files', nuevoNombreFile) 
        file.save(upload_path)
        path_database = f"/static/files/{nuevoNombreFile}"
        data = {
            "id" : request.form["id"],
            "estado" : request.form["proximo_estado"],
            "documento" : path_database
        }
        Trabajo.send(data)
        return redirect('/dashboard')
    else:
        return redirect('/dashboard')

    
@app.route('/usuarios/historial')
def mostrar_historial():
    if session.get('id') == None:
        return redirect('/')
    else:
        session["update"] = "no"
        usuario = Usuario.get_por_id(session['id'])
        funcion = Trabajo
        if usuario.nivel_usuario_id <= 2:
            trabajos = Trabajo.get_all()
            return render_template('historial_trabajos.html', usuario = usuario, trabajos = trabajos, funcion = funcion)
        else:
            trabajos = Trabajo.get_all_user(session['id'])
            return render_template('historial_trabajos.html', usuario = usuario, trabajos = trabajos, funcion = funcion)


@app.route('/usuarios/historial_filtro', methods=['GET', 'POST'])
def mostrar_historial_filtrado():
    if request.method == 'POST':
        session["update"] = "no"
        usuario = Usuario.get_por_id(session['id'])
        funcion = Trabajo
        if usuario.nivel_usuario_id <= 2:
            trabajos = Trabajo.get_all()
            return render_template('admin_historial.html', usuario = usuario, trabajos = trabajos, funcion = funcion)
        else:
            data = {
                "id" : session['id'],
                "titulo": "%%" + request.form["titulo"] + "%%",
                "fecha_inicio" : request.form["fecha_inicio"],
                "fecha_fin": request.form["fecha_fin"]
            }
            trabajos = Trabajo.get_filter_user(data)
            return render_template('cliente_historial.html', usuario = usuario, trabajos = trabajos, funcion = funcion)


@app.route('/cliente/<int:id>')
def mostrar_datos_cliente(id):
    return render_template('cliente_datos.html', usuario = Usuario.get_por_id(session["id"]), cliente = Usuario.get_por_id(id))




