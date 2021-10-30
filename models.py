
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
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
        return Usuarios.get_by_id(int(user_id))

class Peliculas(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    titulo = db.Column(db.String(64))
    genero = db.Column(db.String(16))
    duracion = db.Column(db.Integer())
    clasificacion = db.Column(db.String(20))
    estado = db.Column(db.String(11))
    resena = db.Column(db.String())
    imagen = db.Column(db.String(28))

    def __repr__(self):
        return '<Peliculas {}>'.format(self.id)

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

class Funciones(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    id_sala = db.Column(db.Integer(), db.ForeignKey('salas.id'))
    id_horario = db.Column(db.Integer(), db.ForeignKey('horarios.id_horario'))
    id_pelicula = db.Column(db.Integer(), db.ForeignKey('peliculas.id'))
    valor = db.Column(db.Integer())
    pelicula = db.relationship(Peliculas)
    horarios = db.relationship(Horarios)
    salas = db.relationship(Salas)

    def __repr__(self):
        return '<Funciones {}>'.format(self.id)

class Comentarios(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    id_usuario = db.Column(db.Integer(), db.ForeignKey('usuarios.id'))
    id_pelicula = db.Column(db.Integer(), db.ForeignKey('peliculas.id'))
    calificacion = db.Column(db.Integer(), nullable=False)
    comentario = db.Column(db.String(128))
    usuario = db.relationship(Usuarios)
    pelicula = db.relationship(Peliculas)

    def __repr__(self):
        return '<Comentarios {}>'.format(self.id)

class Ventas(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    id_usuario = db.Column(db.Integer(), db.ForeignKey('usuarios.id'))
    id_pelicula = db.Column(db.Integer(), db.ForeignKey('peliculas.id'))
    num_boletas = db.Column(db.Integer(), nullable=False)
    id_sala = db.Column(db.Integer(), db.ForeignKey('salas.id'))
    id_horario = db.Column(db.Integer(), db.ForeignKey('horarios.id_horario'))
    pelicula = db.relationship(Peliculas)
    usuario = db.relationship(Usuarios)
    sala = db.relationship(Salas)
    horario = db.relationship(Horarios)

    def __repr__(self):
        return '<Comentarios {}>'.format(self.id)
