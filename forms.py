from flask_wtf import FlaskForm
from wtforms import (BooleanField, PasswordField, StringField, SubmitField,
                     TextAreaField, validators)
from wtforms.fields.core import IntegerField
from wtforms.fields.html5 import EmailField
from wtforms.fields.simple import TextField
from wtforms.validators import DataRequired, Email, Length


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4)])
    #remember_me = BooleanField('Recuérdame')
    submit = SubmitField('Ingresar')

class RegistroForm(FlaskForm):
    nombre = StringField('Nombre',validators=[DataRequired()])
    identificacion = StringField('Identificacion',validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4)])
    confirm_paswd = PasswordField('Confirmar Password', validators=[DataRequired(), Length(min=4)])
    #remember_me = BooleanField('Recuérdame')
    submit = SubmitField('Registrarse')
