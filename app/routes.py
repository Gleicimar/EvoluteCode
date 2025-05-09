from flask import Blueprint, flash, render_template, request, flash, get_flashed_messages,redirect, url_for

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')
@main.route('/login',methods=['GET', 'POST'])
def login():
    if request.method =='POST':
        usuario =request.form['username']
        senha = request.form['password']
        if usuario == 'admin' and senha =='admin':
            return redirect(url_for('painel'))
        else:
            flash('Usuário ou senha incorretos')
            return render_template('login.html')
    return render_template('login.html')



@main.route('/painel')
def painel():
    return render_template('painel.html')