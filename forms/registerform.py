from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    login = StringField('Имя пользователя', validators=[DataRequired()])
    hashed_password = StringField('Пароль', validators=[DataRequired()])
    password_again = StringField('Повторите пароль', validators=[DataRequired()])
    admin_code = StringField('Код администратора', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться    ')