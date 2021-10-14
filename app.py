import os
import sqlite3
from sqlite3 import dbapi2

from flask import Flask, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
from wtforms.validators import Email

import db
from forms import LoginForm, RegistroForm
from models import usuario


def get_db_connection():
    conn = sqlite3.connect('cinema.db')
    conn.row_factory = sqlite3.Row
    return conn

listaUser = {'pedrog@hotmail.com':'pedro123','carol@hotmail.com':'carolina123','manueljose@gmail.com':'manuel123'}
listaTipo = {'pedrog@hotmail.com':'user','carol@hotmail.com':'user','manueljose@gmail.com':'admin'}

app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(32)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('formIndex.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method=="GET":
        return render_template('formloguin.html', form=LoginForm())
    else:
        
        formulario = LoginForm(request.form)

        usr = formulario.email.data.replace("'","")
        print(usr)
        pwd = formulario.password.data.replace("'","")

        valor = listaUser.get(usr)
        if valor is not None :
            valoruser = listaTipo.get(usr)
            if valoruser is not None :
                if valoruser == 'admin':
                    return redirect('/admin/peliculas')
                else:
                    return redirect('/usuario/')

        """ obj_usuario = usuario(0,usr,pwd)
        if obj_usuario.autenticar():
            print("la gonorrea corono")
            return redirect('/home/') """
        
        return render_template('formloguin.html', mensaje="Nombre de usuario o contraseña incorrecta.", form=formulario) 
        #return render_template('formLoguin.html', form=form)

@app.route('/registro/', methods=['GET', 'POST'])
def registro():
    form= RegistroForm()
    if request.method == "GET":
        return render_template('formRegistro.html', form= RegistroForm())
    else:
        formRegistro = RegistroForm(request.form)
        name = formRegistro.nombre.data
        identificacion = formRegistro.identificacion.data
        email = request.form['email']
        passwor = formRegistro.password.data
        pswd = formRegistro.confirm_paswd.data
        #print(usr)
        conpsw = formRegistro.confirm_paswd.data
        if (passwor == pswd):
            return redirect('/login')
        else:
            return redirect('/registro/')

        #return render_template('formRegistro.html', form=RegistroForm())

@app.route('/admin/<string:id>')
def admin(id):
    #posts = get_pelicula(id)
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM '+id).fetchall()
    conn.close()
    nombre = id
    return render_template('formadmin.html', posts=posts, nombre=nombre)
@app.route('/admin/')
def adminuser():
    return render_template('formadmin.html')


@app.route('/usuario/')
def usuario():
    return render_template('formUsuario.html')

@app.route('/cartelera/')
def cartelera():
    return render_template('formIndex.html')

@app.route('/funciones/')
def funciones():
    return render_template('formFunciones.html')


@app.route('/comentario/')
def comentario():
    return render_template('formComentario.html')

