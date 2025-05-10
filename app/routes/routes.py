from flask import Blueprint, flash, render_template, request, flash, get_flashed_messages,redirect, session, url_for
from models.mongo import conexao
main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/usuarios')
def listar_usuarios():
    usuario =conexao.usuarios.find()
    return render_template('usuarios.html', usuarios=usuario)

@main.route('/login',methods=['GET', 'POST'])
def login():
    if request.method =='POST':
        usuario =request.form['usuario']
        senha = request.form['senha']
        if usuario == 'admin' and senha =='admin':
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