from flask import Blueprint, render_template, request, flash, get_flashed_messages,redirect, session, url_for
from app.models.user_model import autenticar_usuario, cadastrar_usuario
auth = Blueprint('auth', __name__)


@auth.route('/cadastrar',methods
            =["GET", "POST"]) 
def cadastrar():
    if request.method=='POST':
        usuario= request.form['usuario']
        senha =request.form['senha']
        cadastrar_usuario(usuario,senha)
        flash('Usuario cadastrado com sucesso! :)','success')
    flash('Usuario ja cadastrado!','erro')
    return render_template('cadastrar.html')
@auth.route('/login',methods=['GET', 'POST'])
def login():
    if request.method =='POST':
        usuario =request.form['usuario']
        senha = request.form['senha']
        usuario = autenticar_usuario(usuario,senha) 
        if usuario :
            session['usuario'] = {'nome':usuario.get('usuario'),
                                '_id' : str(usuario.get('_id')) }  # adicionar ao session o nome do usuario
            flash('Login realizado com sucesso! :)','success')
            return redirect(url_for('auth.painel_view'))
        else:
            flash(' :(  Usuário ou senha incorretos!','error')
            return render_template('login.html')
    return render_template('login.html')


@auth.route('/painel')
def painel_view():
    if 'usuario' not in session: 
        redirect(url_for('auth.login'))
    return render_template('home_painel.html')   