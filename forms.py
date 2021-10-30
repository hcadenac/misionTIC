from flask_wtf import FlaskForm
from wtforms import (BooleanField, PasswordField, StringField, SubmitField,
                     TextAreaField, validators)
from wtforms.fields.core import IntegerField, SelectField
from wtforms.fields.html5 import EmailField
from wtforms.fields.simple import TextField
from wtforms.validators import (DataRequired, Email, EqualTo, Length,
                                ValidationError)


class LoginForm(FlaskForm):
    usuario = EmailField('Email', validators=[DataRequired(message='Debe ingresar el usuario'), Email()])
    password = PasswordField('Password', validators=[DataRequired(message='Debe ingresar el password')])
    submit = SubmitField('Ingresar')

class RegistroForm(FlaskForm):
    nombre = StringField('Nombre',validators=[DataRequired(message='Debe ingresar el nombre')])
    usuario = EmailField('Email', validators=[DataRequired(message='Debe ingresar el Email'), Email()])
    password = PasswordField('Password', validators=[DataRequired(message='Debe ingresar el password')])
    confirm_paswd = PasswordField('Confirmar Password', validators=[DataRequired(message='Debe ingresar el password'), EqualTo('password', 'Las contraseñas no coinciden')])
    tipo = StringField('Tipo Usuario', validators=[DataRequired(message='Debe ingresar el nombre')])
    submit = SubmitField('Registrarse')

class addForm(FlaskForm):
    titulo = StringField('Titulo',validators=[DataRequired(message='Debe ingresar el titulo')])
    genero = StringField('Genero', validators=[DataRequired(message='Debe ingresar el genero'), Email()])
    duracion = StringField('Duracion', validators=[DataRequired()])
    clasificacion = StringField('Clasificacion', validators=[DataRequired(message='Debe ingresar la clasificacion')])
    estado = StringField('Estado',validators=[DataRequired(message='Debe ingresar el estado')])
    resena = TextAreaField('Reseña',validators=[DataRequired(message='Debe ingresar la reseña')])
    
    opcion = SelectField('Seleccione la Opcion', choices=[])
    calificacion = IntegerField('Calificacion', validators=[DataRequired(message='Debe ingresar la calificacion')])
    comentario = TextAreaField('Comentario',validators=[DataRequired(message='Debe ingresar Comentario')])

    dia = StringField('Dia',validators=[DataRequired(message='Debe ingresar el dia')])
    hora_funcion = StringField('Hora de la Funcion',validators=[DataRequired(message='Debe ingresar la hora')])

    nombre_sala= StringField('Nombre Sala',validators=[DataRequired(message='Debe ingresar el nombre')])
    capacidad = IntegerField('Capacidad', validators=[DataRequired(message='Debe ingresar el nombre'), Length(min=1, max= 3)])
    #remember_me = BooleanField('Recuerdame')
    submit = SubmitField('Guardar Registro')

    id_sala= IntegerField('ID SALA', validators=[DataRequired()])
    id_horario= StringField('ID HORARIO', validators=[DataRequired()])
    id_pelicula= IntegerField('ID PELICULA', validators=[DataRequired()])
    valor= IntegerField('VALOR DE LA FUNCION', validators=[DataRequired()])

class gestionForm(FlaskForm):
    opcion = SelectField('Seleccione la Opcion', choices=[('peliculas','Peliculas'),('usuarios','Usuarios'),('funciones','Funciones'),('horarios','Horarios'),('salas','Salas')])
    submit = SubmitField('Seleccionar')
    
