import os
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_wtf.csrf import CSRFProtect
from app.forms import RegistrationForm
from app.models import User, init_db

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-cambiar')

    csrf = CSRFProtect(app)
    init_db()  # Inicializar base de datos

    @app.route("/")
    def index():
        return "¡Bienvenido a ZunekoApp!"

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        form = RegistrationForm()
        if form.validate_on_submit():
            if User.get_by_email(form.email.data):
                flash('Ese email ya está registrado.', 'danger')
            else:
                User.create(form.email.data, form.password.data)
                flash('Usuario creado correctamente. Ahora podés iniciar sesión.', 'success')
                return redirect(url_for('index'))
        return render_template('register.html', form=form)

    return app
