import os
import sqlite3
from sqlite3 import dbapi2
from typing import Text

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import (LoginManager, current_user, login_required,
                         login_user, logout_user)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import abort
from wtforms.validators import Email

import db
#from app import app
from forms import LoginForm, RegistroForm, addForm, gestionForm


def get_db_connection():
    conn = sqlite3.connect('cinema.db')
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(32)
DEBUG = True
app.config['SQLALCHEMY_DATABASE_URI']  = 'sqlite:///cinema.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
login_manager = LoginManager(app)
#login_manager.login_view = "login"
login_manager.init_app(app)
db = SQLAlchemy(app)

from models import (Comentarios, Funciones, Horarios, Peliculas, Salas,
                    Usuarios, Ventas)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('formIndex.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    #form = FormInicio()
    if form.validate_on_submit():
        usuario = Usuarios.query.filter_by(usuario=form.usuario.data).first()
        if usuario:
            if usuario.verif_clave(form.password.data):
                login_user(usuario, 'True')
                tipo = usuario.tipo
                print(tipo)
                if (tipo == 'user'):
                    return redirect(url_for('usuario'))
                else:
                    return redirect(url_for('admin', id='peliculas'))
            else:
                return render_template('formloguin.html', mensaje="    Usuario o contraseña Invalido.", form=LoginForm())#return redirect(url_for('index'))
    return render_template('formloguin.html', form=form) 

@app.route('/registro/', methods=['GET', 'POST'])
def registro():
    form= RegistroForm()
    if request.method == "GET":
        return render_template('formRegistro.html', form= RegistroForm())
    else:
        if form.validate_on_submit():
            usuarios = Usuarios(nombre=form.nombre.data, usuario=form.usuario.data, tipo="user")
            clave = form.password.data
            usuarios.def_clave(clave)
            db.session.add(usuarios)
            db.session.commit()
            flash('Usuario registrado correctamente, ahora puedes iniciar sesión.')
            return redirect(url_for('login'))
    return render_template('formRegistro.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/admin/<string:id>', methods=['GET', 'POST'])
def admin(id):
    form= gestionForm()
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM '+id).fetchall()
    conn.close()
    nombre = id
    if request.method == 'POST':
        opcion = form.opcion.data
        conn = get_db_connection()
        posts = conn.execute('SELECT * FROM '+opcion).fetchall()
        conn.close()
        nombre= opcion
        return render_template('formadmin.html', posts=posts, nombre=nombre, form=form)
    else:
        return render_template('formadmin.html', posts=posts, nombre=nombre, form=form)

        
@app.route('/admin/')
def adminuser():
    return render_template('formadmin.html')

##adicionar datos#####
@app.route('/add/<string:id>', methods = ['GET', 'POST'])
def addOpcion(id):
    nombre = id 
    form= addForm()
    if request.method == 'POST':
        if (id == 'peliculas'):
            pelicula = Peliculas(titulo=form.titulo.data, genero=form.genero.data, duracion=form.duracion.data, clasificacion=form.clasificacion.data, estado=form.estado.data, resena=form.resena.data)
            db.session.add(pelicula)
            db.session.commit()
            flash("...Registro Ingresado con Exito...")
            return redirect(url_for('admin', id='peliculas'))
        elif(id == 'horarios'):
            horario = Horarios(id_horario=form.id_horario.data, dia=form.dia.data, hora_fun=form.hora_funcion.data)
            db.session.add(horario)
            db.session.commit()
            flash("...Registro Ingresado con Exito...")
            return redirect(url_for('admin', id='horarios'))
        elif(id == 'funciones'):
            funcion = Funciones(id_sala=form.id_sala.data, id_horario=form.id_horario.data, id_pelicula=form.id_pelicula.data, valor=form.valor.data)
            db.session.add(funcion)
            db.session.commit()
            flash("...Registro Ingresado con Exito...")
            return redirect(url_for('admin', id='funciones'))
        elif(id == 'salas'):
            sala = Salas(nombre=form.nombre_sala.data, capacidad=form.capacidad.data)
            db.session.add(sala)
            db.session.commit()
            flash("...Registro Ingresado con Exito...")
            return redirect(url_for('admin', id='salas'))

        else:
            return redirect(url_for('admin', id='peliculas'))
    else:
        return render_template('formAdd.html', nombre= nombre, form=form)
  
@app.route('/add', methods = ['GET', 'POST'])
def add():
    form= addForm()
    if request.method == 'POST':
        pelicula = Peliculas(titulo=form.titulo.data, genero=form.genero.data, duracion=form.duracion.data, clasificacion=form.clasificacion.data, estado=form.estado.data, resena=form.resena.data)
        db.session.add(pelicula)
        db.session.commit()
        return redirect(url_for('admin', id='peliculas'))
    else:
        return render_template('formAdd.html', form=form)

####Borrar datos en las tablas######
@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    lista = id.split(" ")
    if (lista[0] == 'peliculas'):
        datos = Peliculas.query.get(lista[1])
        db.session.delete(datos)
        db.session.commit()
        flash("..Registro Borrado con Exito...")
        return redirect(url_for('admin', id='peliculas'))
    elif (lista[0] == 'usuarios'):
        datos = Usuarios.query.get(lista[1])
        db.session.delete(datos)
        db.session.commit()
        flash("..Registro Borrado con Exito")
        return redirect(url_for('admin', id='usuarios'))
    elif (lista[0] == 'funciones'):
        datos = Funciones.query.get(lista[1])
        db.session.delete(datos)
        db.session.commit()
        flash("..Registro Borrado con Exito")
        return redirect(url_for('admin', id='funciones'))
    elif (lista[0] == 'horarios'):
        datos = Horarios.query.get(lista[1])
        db.session.delete(datos)
        db.session.commit()
        flash("..Registro Borrado con Exito")
        return redirect(url_for('admin', id='horarios'))
    elif (lista[0] == 'salas'):
        datos = Salas.query.get(lista[1])
        db.session.delete(datos)
        db.session.commit()
        flash("..Registro Borrado con Exito")
        return redirect(url_for('admin', id='salas'))

###### Editar Registros en la base de datos ###################
@app.route("/update/<string:dato>", methods = ['GET', 'POST'])
def update(dato):
    form= addForm()
    datas = db.session.query(Peliculas).filter(Peliculas.id == 1).all()
    lista = dato.split(" ")
    if (lista[0] == 'salas'):
        datos = Salas.query.get(lista[1])
        if request.method == "GET": 
            nombre = 'salas'
            return render_template('formEdit.html', nombre=nombre, dato1=datos.nombre, dato2=datos.capacidad, form=form)
        elif request.method == "POST":
            datos = Salas.query.get(lista[1])
            datos.nombre=form.nombre_sala.data
            datos.capacidad = form.capacidad.data
            db.session.commit()
            flash("..Registro Editado con Exito..")
            return redirect(url_for('admin', id='salas'))  
    elif (lista[0] == 'peliculas'):
        datos = Peliculas.query.get(lista[1])
        if request.method == "GET": 
            nombre = 'peliculas'
            id = lista[1]
            return render_template('formEdit.html', nombre=nombre, dato1=datos.titulo, dato2=datos.genero, dato3=datos.duracion, dato4=datos.clasificacion, dato5=datos.estado, form=form)
        elif request.method == "POST":
            datos.titulo=form.titulo.data
            datos.genero = form.genero.data
            datos.duracion=form.duracion.data
            datos.clasificacion=form.clasificacion.data
            datos.estado=form.estado.data
            db.session.commit()
            flash("..Registro Editado con Exito..")
            return redirect(url_for('admin', id='peliculas'))  
    elif (lista[0] == 'usuarios'):
        form= RegistroForm()
        datos = Usuarios.query.get(lista[1])
        if request.method == "GET": 
            nombre = 'usuarios'
            return render_template('formEdit.html', nombre=nombre, dato1=datos.nombre, dato2=datos.usuario, dato3=datos.tipo, form=form)
        elif request.method == "POST":
            datos.nombre=form.nombre.data
            datos.usuario = form.usuario.data
            datos.tipo=form.tipo.data
            db.session.commit()
            flash("..Registro Editado con Exito..")
            return redirect(url_for('admin', id='usuarios'))     
    elif (lista[0] == 'funciones'):
        #form= RegistroForm()
        datos = Funciones.query.get(lista[1])
        if request.method == "GET": 
            nombre = 'funciones'
            return render_template('formEdit.html', nombre=nombre, dato1=datos.id_sala, dato2=datos.id_horario, dato3=datos.id_pelicula, dato4=datos.valor, form=form)
        elif request.method == "POST":
            #my_data = Peliculas.query.get(lista[1])
            datos.nombre=form.id_sala.data
            datos.usuario = form.id_horario.data
            datos.tipo=form.id_pelicula.data
            datos.valor=form.valor.data
            db.session.commit()
            flash("..Registro Editado con Exito..")
            return redirect(url_for('admin', id='funciones'))   
    elif (lista[0] == 'horarios'):
        #form= RegistroForm()
        datos = Horarios.query.get(lista[1])
        if request.method == "GET": 
            nombre = 'horarios'
            return render_template('formEdit.html', nombre=nombre, dato1=datos.id_horario, dato2=datos.dia, dato3=datos.hora_fun, form=form)
        elif request.method == "POST":
            #my_data = Peliculas.query.get(lista[1])
            datos.id_horario=form.id_horario.data
            datos.dia = form.dia.data
            datos.hora_fun=form.hora_funcion.data
            db.session.commit()
            flash("..Registro Editado con Exito..")
            return redirect(url_for('admin', id='horarios'))   
    else:
        return render_template('formAdmin.html', nombre='peliculas', form=form)

@app.route('/usuario', methods = ['GET', 'POST'])
def usuario():
    conn = get_db_connection()
    datos = conn.execute('SELECT titulo FROM peliculas').fetchall()
    conn.close()
    if request.method == 'GET':
        return render_template('formUsuario.html', datos=datos)
    elif request.method == 'POST':
        titulo = request.form['pelicula']
        listaP = db.session.query(Peliculas.id ).filter(Peliculas.titulo ==titulo).all()
        #print(listaP[0][0])
        id =(listaP[0][0]) #my_data.email = request.form['email']
        dia = request.form['dia']
        #print(dia)
        my_data = (db.session.query(Peliculas.id, Peliculas.titulo, Horarios.dia, Horarios.hora_fun, Salas.nombre, Funciones.valor)
                .filter(Peliculas.id == Funciones.id_pelicula)
                .filter(Funciones.id_horario == Horarios.id_horario)
                .filter(Funciones.id_sala == Salas.id)
                .filter(Horarios.dia == dia)
                .filter(Peliculas.id == id).all())
        #print(my_data[0][0])
        if (len(my_data) == 0):
            flash("La consulta no encontro registros disponibles")
            return render_template('formUsuario.html', datos=datos)
        else:
            return render_template('formUsuario.html', datos=datos, lista=my_data, nombre=titulo)
        #my_data.phone = request.form['phone']
            

    #texto = 'todos son unas gonorreas'
    #return render_template('formUsuario.html')

@app.route('/ventas/<id>',  methods = ['GET', 'POST'])
def ventas(id):
    #print(id)
    conn = get_db_connection()
    datos = conn.execute('SELECT titulo FROM peliculas').fetchall()
    conn.close()
    if request.method == 'GET':
        if current_user.is_authenticated:
        #usuario = current_user.nombre
        #print(current_user.id)
            venta = Ventas(id_usuario=current_user.id, id_pelicula=id, num_boletas = 1)
            db.session.add(venta)
            db.session.commit()
            flash("La compra se ha realizado con exito")
        else:
            flash("El usaurio no esta autenticado en la plataforma")
            return redirect(url_for('login')) 
        return render_template('formUsuario.html', datos=datos)

@app.route('/cartelera/')
def cartelera():
    return render_template('formIndex.html')

@app.route('/funciones/')
def funciones():
    return render_template('formFunciones.html')

##### Consulta de Comentarios  ###############
@app.route('/comentario/', methods = ['GET', 'POST'])
def comentario():
    conn = get_db_connection()
    datos = conn.execute('SELECT DISTINCT peliculas.titulo FROM peliculas, comentarios WHERE peliculas.id = comentarios.id_pelicula').fetchall()
    conn.close()
    if request.method == 'POST':
        pelicula = request.form['pelicula']
        listaP = db.session.query(Peliculas.id ).filter(Peliculas.titulo == pelicula).all()
        id =(listaP[0][0]) 
        listaC = (db.session.query(Usuarios.usuario, Comentarios.calificacion, Comentarios.comentario)
                .filter(Usuarios.id == Comentarios.id_usuario)
                .filter(Comentarios.id_pelicula == id).all())
        #print(listaC)
        return render_template('formComentario.html', datos=datos, lista=listaC)
    else:
        return render_template('formComentario.html', datos=datos)

#### Gestion de Comentarios ###########
@app.route('/gestionComentario/', methods = ['GET', 'POST'])
def gestionComentario():
    if current_user.is_authenticated:
        user = current_user.id
        listaC = (db.session.query(Comentarios.id, Peliculas.titulo, Comentarios.calificacion, Comentarios.comentario)
                .filter(Peliculas.id == Comentarios.id_pelicula)
                .filter(Comentarios.id_usuario == user).all())
        #print(listaC)
        return render_template('formAdminUser.html', lista=listaC)

######## Editar Comentarios ##########
@app.route('/editComentario/', methods = ['GET', 'POST'])
def editComentario():
    if request.method == 'POST':
        my_data = Comentarios.query.get(request.form['id'])
        my_data.calificacion = request.form['calificacion']
        my_data.comentario = request.form['comentario']
        print(request.form['id'])
        print(my_data.calificacion)
        print(my_data.comentario)
        db.session.commit()
        flash("Comentario Actalizado Con Exito")
        user = current_user.id
        listaC = (db.session.query(Comentarios.id, Peliculas.titulo, Comentarios.calificacion, Comentarios.comentario)
                .filter(Peliculas.id == Comentarios.id_pelicula)
                .filter(Comentarios.id_usuario == user).all())
        return render_template('formAdminUser.html', lista=listaC)
        
        #return render_template('formAdminUser.html')
        #return redirect(url_for('gestionComentario'))
    else:
        return render_template('formAdminUser.html')

#### Borrar Comentarios #########
@app.route('/borraComentario/<id>', methods = ['GET', 'POST'])
def borraComentario(id):
    my_data = Comentarios.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Comentario Borrado con Exito")
    return redirect(url_for('gestionComentario'))

########## Adicionar Comentarios ############
@app.route('/addComentario/', methods = ['GET', 'POST'])
def addComentario():
    dato = 11
    listaP = (db.session.query(Peliculas.titulo)
                .filter(Peliculas.id == Ventas.id_pelicula)
                .filter(Ventas.id_usuario == dato).all())
    print('Gonorrea')
    print(listaP)
    return redirect(url_for('gestionComentario'))

##### funcion user loader######
@login_manager.user_loader
def get_user(user_id):
    try:
        return Usuarios.query.get(int(user_id))
    except:
        return None
