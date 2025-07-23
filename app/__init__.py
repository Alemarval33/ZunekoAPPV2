from flask import Flask, render_template, redirect, url_for, flash, request
from app.forms import RegistrationForm
from app.models import User

def create_app():
    app = Flask(__name__)

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
                user = User.create(form.email.data, form.password.data)
                flash('Usuario creado correctamente. Ahora podés iniciar sesión.', 'success')
                return redirect(url_for('login'))
        return render_template('register.html', form=form)

    return app
