from flask import Blueprint, flash, render_template, request, flash, get_flashed_messages,redirect, session, url_for
from app.models.user_model import autenticar_usuario
main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')



@main.route('/login',methods=['GET', 'POST'])
def login():
    if request.method =='POST':
        usuario =request.form['usuario']
        senha = request.form['senha']
        usuario =autenticar_usuario(usuario,senha)
        if usuario is not None:
            session['usuario'] = usuario  # adicionar ao session o nome do usuario
            return redirect(url_for('main.painel_view'))
        else:
            flash('Usuário ou senha incorretos')
            return render_template('login.html')
    return render_template('login.html')



@main.route('/painel')
def painel_view():
    if 'usuario' not in session: 
        redirect(url_for('main.login'))
    return render_template('home_painel.html')  