from flask import Blueprint, render_template, request, flash, get_flashed_messages,redirect, session, url_for
from app.models.user_model import autenticar_usuario, cadastrar_usuario
import bcrypt
import bleach


auth = Blueprint('auth', __name__)


@auth.route('/cadastrar',methods=["GET", "POST"]) 
def cadastrar():
    if request.method=='POST':
        usuario= request.form['usuario'].strip()
        senha =request.form['senha'].strip()
        confirmar_senha = request.form['confirmar_senha'].strip
        #sanitização de acessos
        usario = bleach.clean(usuario)
        senha = senha
        confirmar_senha =confirmar_senha

        if not usuario or senha or confirmar_senha: 
            flash(" 😒Por favor preencha todos os campos 👌 , erro")
        if len(senha) < 6:
            flash(" A 🔐 Senha 🔐 deve ter pelo menos 6 caracteres, erro")
        cadastrar_usuario(usuario,senha)
        flash('Usuario cadastrado com sucesso! 😊','success')
    flash('Usuario ja cadastrado!','erro')
    return render_template('cadastrar.html')
@auth.route('/login',methods=['GET', 'POST'])

#Configuração inicial 
MAX_LOGIN_ATTEMPTS= 5
LOCKOUT_TIME =300 #5 minutos para bloqueio

def login():
    if request.method =='POST': 
        session.clear()
        usuario_input = bleach.clean(request.form['usuario'])
        senha = request.form['senha'].strip()
        if 'login_attempts' not in session:
            session['login_attempts']= 0
            sesion['lockout_time'] = None
        if session.get('lockout_time'):
            if time.time() < session['lockout_time']:
                flash("Você excedeu o numero de tentativas . Tente novamente em alguns minutos, erro")
                return('login')
        else:
            session['login_attempts']= 0
            session['lockout_time'] =None

        if not usuario_input or senha : 
            flash(" 😒Por favor preencha todos os campos 👌 , erro")
        usuario = autenticar_usuario(usuario_input,senha) 
        if usuario :
            session['usuario'] = { 'nome': usuario.get('nome') or usuario.get('usuario'),  # Usa o nome, senão o login,
                                '_id' : str(usuario.get('_id')) } 
            flash('Login realizado com sucesso! 😊😊 ','success')
            return redirect(url_for('auth.painel_view'))
        else:
            flash('😭😭😭 Usuário ou senha incorretos!','error')
    return render_template('login.html')

@auth.route('/painel')
@login_required
def painel_view():
    if 'usuario' not in session: 
        flash('😭😭😭 Você prexcisa estar logado!','error')
        return
    redirect(url_for('auth.login'))
    nome_usuario=session['usuario']['nome']
    return render_template('home_painel.html', nome=nome_usuario ) 
