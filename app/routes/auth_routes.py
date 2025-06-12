from flask import Blueprint, render_template, request, flash, get_flashed_messages,redirect, session, url_for
from app.models.user_model import autenticar_usuario, cadastrar_usuario, User
from flask_login import login_user, login_required
import bcrypt
import bleach
import time 


auth = Blueprint('auth', __name__)

#Configuração inicial 
MAX_LOGIN_ATTEMPTS= 5
LOCKOUT_TIME =300 #5 minutos para bloqueio

@auth.route('/cadastrar',methods=["GET", "POST"]) 
def cadastrar():
    if request.method == 'POST':
       
        usuario = request.form['usuario'].strip()
        senha = request.form['senha'].strip()
        confirmar_senha = request.form['confirmar_senha'].strip()
        #sanitização de acessos
        usuario = bleach.clean(usuario)
        senha = senha
        confirmar_senha = confirmar_senha

        if not usuario or not senha or not confirmar_senha: 
            flash(" 😒Por favor preencha todos os campos 👌 , erro")
            if len(senha) < 6:
                flash(" A 🔐 Senha 🔐 deve ter pelo menos 6 caracteres, erro")
            if senha != confirmar_senha:
                flash("🔐 As senhas não coincidem!", 'error')
                return render_template('cadastrar.html')
            cadastrar_usuario(usuario,senha)

            sucesso = cadastrar_usuario(usuario, senha)
            if sucesso:
                flash('✅ Usuário cadastrado com sucesso! 😊', 'success')
                return redirect(url_for('auth.login'))
            else:
                flash('⚠️ Usuário já cadastrado!', 'error')
    return render_template('cadastrar.html')

@auth.route('/login',methods=['GET', 'POST'])
def login():
    if request.method =='POST': 
        usuario_input = bleach.clean(request.form['usuario'])
        senha = request.form['senha'].strip()
        if 'login_attempts' not in session:
            session['login_attempts']= 0
            session['lockout_time'] = None
        if session.get('lockout_time'):
            if time.time() < session['lockout_time']:
                flash("Você excedeu o numero de tentativas . Tente novamente em alguns minutos, erro")
            return redirect(url_for('auth.login'))
        else:
            session['login_attempts']= 0
            session['lockout_time'] =None

        if not usuario_input or not senha : 
            flash("😒Por favor preencha todos os campos" , "error")
        usuario = autenticar_usuario(usuario_input,senha) 

        if usuario :
            session['usuario'] = { 'nome': usuario.get('nome') or usuario.get('usuario'),  # Usa o nome, senão o login,
                                '_id' : str(usuario.get('_id')) } 
            login_user(User(usuario))

            session['login_attempts'] = 0  # Zera tentativas
            flash('✅ Login realizado com sucesso! 😊😊', 'success')
            return redirect(url_for('auth.painel_view'))
        else:
            session['login_attempts'] += 1
            if session['login_attempts'] >= MAX_LOGIN_ATTEMPTS:
                session['lockout_time'] = time.time() + LOCKOUT_TIME
                flash("🚫 Muitas tentativas. Tente novamente em 5 minutos.", 'error')
            else:
                flash('😭 Usuário ou senha incorretos!', 'error')

    return render_template('login.html')
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    flash("🔒 Logout realizado com sucesso.", 'success')
    return redirect(url_for('auth.login'))

@auth.route('/painel')
@login_required
def painel_view():
    if 'usuario' not in session: 
        flash('😭😭😭 Você precisa estar logado!','error')
        return
        redirect(url_for('auth.login'))
    nome_usuario=session['usuario']['nome']
    return render_template('home_painel.html', nome=nome_usuario ) 

@auth.route('/consulta_projetos')
@login_required

def consulta_projeto():
    if projetos =
