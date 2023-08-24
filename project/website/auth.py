from flask import Blueprint, render_template, url_for, request, flash, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from website import db
from flask_login import login_user, logout_user
auth = Blueprint('auth', __name__)

@auth.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup',  methods=['GET', 'POST'])
def signUp():
    if request.method == 'GET':
        return render_template("auth/signUp.html")
    
    if request.method == 'POST':
        name =  request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        password_confirmation = request.form.get('password-confirmation')
        print(password_confirmation, password)
        # dictin = {
        #     'nome': request.form.get('nome'),
        #     'email': request.form.get('email')
        # }

        user = User.query.filter_by(email=email).first()#pega o primeiro usuario com o email
        if user:
            flash('Email already exists.', category='error')

        elif not email or len(email) <6:
            flash('Email deve ter mais de 6 caracteres.', category='error')
        elif not name or len(name) <2:
            flash('Nome deve ter mais de 2 caracteres.', category='error')
        elif  password != password_confirmation:
            flash('Password Doest Match.', category='error')
        elif not password or len(password) <7:
            flash('Must Contain a lenght of 7.', category='error')
        else:
            user = User(email=email, name=name, password= generate_password_hash(password, method='sha256'))
            db.session.add(user)#adiciona o usuario no banco de dados
            db.session.commit()#confirma que adicionou
            login_user(user, remember=True)
            flash('The account was created successfuly', category='success')
            return redirect(url_for('views.home'))
    return render_template("auth/login.html")
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("auth/login.html")
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()#pega o primeiro usuario com o email

        if user:
            if check_password_hash(user.password, password):
                flash('Login was Successful!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Wrong Password.', category='error')
        else:
            flash('Email does not exist.', category='error')


       
    return render_template("auth/login.html")