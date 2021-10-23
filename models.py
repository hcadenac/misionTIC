from flask_login import UserMixin
from werkzeug.security import check_password_hash as checkph
from werkzeug.security import generate_password_hash as genph

from app import db


class Usuarios(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    nombre = db.Column(db.String(64))
    usuario = db.Column(db.String(50), index=True, unique=True)
    password = db.Column(db.String(150))
    tipo = db.Column(db.String(5))

    def __repr__(self):
        return '<Usuario {}>'.format(self.usuario)

    def def_clave(self, clave):
        self.password = genph(clave)

    def verif_clave(self, clave):
        return checkph(self.password, clave)
    
    def get_id(self):
           return (self.id)

    def load_user(user_id):
    #return Usuarios.query.filter_by(usuario=usuario).first()
        return Usuarios.get_by_id(int(user_id))

class Peliculas(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    titulo = db.Column(db.String(64))
    genero = db.Column(db.String(16))
    duracion = db.Column(db.Integer())
    clasificacion = db.Column(db.String(20))
    estado = db.Column(db.String(11))
    resena = db.Column(db.String())

    def __repr__(self):
        return '<Peliculas {}>'.format(self.id)

class Funciones(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    id_sala = db.Column(db.Integer(), db.ForeignKey('salas.id'))
    id_horario = db.Column(db.Integer(), db.ForeignKey('horarios.id_horario'))
    id_pelicula = db.Column(db.Integer(), db.ForeignKey('peliculas.id'))
    valor = db.Column(db.Integer())

    def __repr__(self):
        return '<Funciones {}>'.format(self.id)

class Horarios(db.Model):
    id_horario = db.Column(db.String(12), primary_key=True)
    dia = db.Column(db.String(12))
    hora_fun = db.Column(db.String(12), nullable=False)

    def __repr__(self):
        return '<Horarios {}>'.format(self.dia)

class Salas(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    nombre = db.Column(db.String(12))
    capacidad = db.Column(db.Integer(), nullable=False)

    def __init__(self, nombre, capacidad):
        self.nombre = nombre
        self.capacidad = capacidad

class Comentarios(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    id_usuario = db.Column(db.Integer(), db.ForeignKey('usuarios.id'))
    id_pelicula = db.Column(db.Integer(), db.ForeignKey('peliculas.id'))
    calificacion = db.Column(db.Integer(), nullable=False)
    comentario = db.Column(db.String(128))

    def __repr__(self):
        return '<Comentarios {}>'.format(self.id_usuario)

class Ventas(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    id_usuario = db.Column(db.Integer(), db.ForeignKey('usuarios.id'))
    id_pelicula = db.Column(db.Integer(), db.ForeignKey('peliculas.id'))
    num_boletas = db.Column(db.Integer(), nullable=False)
    #total_venta = db.Column(db.Integer(), nullable=False)

    def __repr__(self):
        return '<Comentarios {}>'.format(self.id_usuario)




#####Clase para manejar los usuarios
""" class Usuario():
    nombre=''
    usuario=''
    password=''
    tipo=''

    def __init__(self, pnombre, pusuario, ppassword): 
        self.nombre = pnombre
        self.usuario = pusuario
        self.password = ppassword
    
    #Metodo para verificar el usuario contra la base de datos
    def autenticar(self):
        sql = "SELECT * FROM usuarios WHERE usuario = ? AND password = ?;"
        obj = db.ejecutar_select(sql, [self.usuario, self.password])
        if obj:
            if len(obj) >0:
                return True
        return False """
#################################
