from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    login = StringField(label="Логин", validators=[DataRequired()])
    password = PasswordField(label="Пароль", validators=[DataRequired()])
    remember_me = BooleanField(label="Запомнить меня")
    submit_button = SubmitField(label="Войти")
    register_button = SubmitField(label="Зарегестрироваться")