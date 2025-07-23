import os
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_mail import Mail
from flask_wtf import CSRFProtect
from app.forms import RegistrationForm
from app.models import User, init_db

mail = Mail()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'devkey')
    app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
    app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 465))
    app.config['MAIL_USE_SSL'] = os.environ.get('MAIL_USE_SSL', 'True') == 'True'
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')

    mail.init_app(app)
    csrf.init_app(app)
    init_db()  # Inicializa la DB en la primer petición

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
