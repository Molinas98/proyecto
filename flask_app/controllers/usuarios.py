from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_bcrypt import Bcrypt
from ..models.usuario import Usuario
from ..models.trabajo import Trabajo
from ..models.trabajo_asignado import Trabajo_asignado
from base64 import b64encode
from PIL import Image

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def mostrar_dashboard():
    if session.get('id') == None:
        return redirect('/')
    else:
        session["update"] = "no"
        usuario = Usuario.get_por_id(session['id'])
        funcion = Trabajo
        if usuario.nivel_usuario_id == 1 or usuario.nivel_usuario_id == 2:
            trabajos = Trabajo.get_all()
            trabajos_asignados = Trabajo_asignado.get_all()
            return render_template('admin_principal.html', usuario = usuario, trabajos=trabajos, funcion = funcion, trabajos_asignados = trabajos_asignados)
        elif (usuario.nivel_usuario_id == 3):
            trabajos = Trabajo.get_all_user(session['id'])
            return render_template('cliente_principal.html', usuario = usuario, trabajos=trabajos, funcion = funcion)
        else:
            return redirect("/")

@app.route('/process', methods=['GET', 'POST'])
def registrar_usuario():
    if request.method == 'POST':
        if not Usuario.validar_registro(request.form):
            flash("El email ya está registrado")
            return redirect('/')
        data = {
            "nombre":request.form['nombre'],
            "apellido" : request.form['apellido'],
            "email" : request.form['email'],
            "password" : bcrypt.generate_password_hash(request.form['password']),
            "celular" : request.form['celular'],
            "nivel_usuario_id" : 3
        }
        session['id'] = Usuario.save(data)
        return redirect('/dashboard')
    else:
        return redirect('/')
    
@app.route('/process_empleado', methods=['GET', 'POST'])
def registrar_empleado():
    if request.method == 'POST':
        if not Usuario.validar_registro(request.form):
            flash("El email ya está registrado")
            return redirect('/usuarios')
        data = {
            "nombre":request.form['nombre'],
            "apellido" : request.form['apellido'],
            "email" : request.form['email'],
            "password" : bcrypt.generate_password_hash(request.form['password']),
            "celular" : request.form['celular'],
            "nivel_usuario_id" : 2
        }
        Usuario.save(data)
        return redirect('/usuarios')
    else:
        return redirect('/usuarios')

@app.route('/update_empleado', methods=['GET', 'POST'])
def actualizar_empleado():
    if request.method == 'POST':
        if request.form['password'] == "":
            data = {
                "nombre":request.form['nombre'],
                "apellido" : request.form['apellido'],
                "email" : request.form['email'],
                "celular" : request.form['celular'],
                "id" : session["empleado_id"]
            }
        else:
            data = {
                "nombre":request.form['nombre'],
                "apellido" : request.form['apellido'],
                "email" : request.form['email'],
                "password" : bcrypt.generate_password_hash(request.form['password']),
                "celular" : request.form['celular'],
                "id": session["empleado_id"]
            }
        Usuario.update(data)
        return redirect('/usuarios')
    else:
        return redirect('/usuarios')

@app.route('/update_estado' , methods=['GET', 'POST'])
def modificar_estado():
    if request.method == 'POST':
        data = {
            "id" : request.form["empleado_id"],
            "estado": request.form["estado"]
        }
        Usuario.update_estado(data)
        return redirect('/usuarios')
    else:
        return redirect('/usuarios')

@app.route('/usuarios')
def gestionar_usuarios():
    if session.get('id') == None:
        return redirect('/')
    else:
        if ("actualizar_pulsado" in session):
            session["update"] = "si"
            session.pop("actualizar_pulsado")
        else:
            session["update"] = "no"
        usuario = Usuario.get_por_id(session['id'])
        if usuario.nivel_usuario_id == 1:
            empleados = Usuario.get_empleados()
            if session["update"] == "si":
                empleado = Usuario.get_por_id(session["empleado_id"])
                return render_template("admin_usuarios.html", usuario = usuario, empleados = empleados, empleado = empleado)
            else:
                return render_template("admin_usuarios.html", usuario = usuario, empleados = empleados)
            
        else:
            return redirect('/dashboard')
        
@app.route('/update_activate', methods=['GET', 'POST'])
def habilitar_edicion():
        if request.method == 'POST':
            session["actualizar_pulsado"] = "si"
            session["update"] = "si"
            session["empleado_id"] = request.form["empleado_id"]
            return redirect("/usuarios")
        else:
            return redirect("/usuarios")

@app.route('/login', methods=['GET', 'POST'])
def iniciar_sesion():
    if request.method == 'POST':
        data = {
            "email" : request.form['login_email']
        }
        user = Usuario.get_por_correo(data)
        password = request.form.get("login_password")
        if user == None:
            flash("El email no está registrado.")
            return redirect('/')
        if user.activo == 0:
            flash("El usuario está deshabilitado.")
            return redirect('/')
        if not bcrypt.check_password_hash(user.password, password):
            flash("Contraseña incorrecta.")
            return redirect('/')
        session["id"] = user.id
        return redirect('/dashboard')
    else:
        return redirect('/')

@app.route('/logout')
def cerrar_sesion():
    session.clear()
    return redirect('/')
