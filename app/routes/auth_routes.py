from flask import Blueprint, render_template, request, flash, get_flashed_messages,redirect, session, url_for
from app.models.user_model import autenticar_usuario, cadastrar_usuario as cadastrar_usuario_model, registrar_usuario, User
from flask_login import login_user, login_required
import bcrypt
import bleach
import time 
from flask_login import logout_user
from app.services.crm_service import CRMService
from app.models.mongo import db  # db pode ser o objeto mongo.db
from app.services.oportunidade_service import listar_oportunidades_service
from app.services.projeto_service import ProjetoService

auth = Blueprint('auth', __name__)

#Configuração inicial 
MAX_LOGIN_ATTEMPTS= 5
LOCKOUT_TIME =300 #5 minutos para bloqueio
crm_service = CRMService()

@auth.route('/painel/cadastrar_usuarios',methods=["GET", "POST"]) 
def cadastrar_usuario_painel():
    if request.method == 'POST':
       
        usuario = request.form['usuario'].strip()
        senha = request.form['senha'].strip()
        cargo = request.form['cargo'].strip()
        confirmar_senha = request.form['confirmar_senha'].strip()
        #sanitização de acessos
        usuario = bleach.clean(usuario)
        senha = senha
        confirmar_senha = confirmar_senha
        cargo = bleach.clean(cargo)

        if not usuario or not senha or not confirmar_senha:
                flash("😒 Por favor preencha todos os campos!", "error")
                return render_template('cadastrar_usuarios.html')

        if len(senha) < 6:
            flash("A senha deve ter pelo menos 6 caracteres.", "error")
            return render_template('cadastrar_usuarios.html')

        if senha != confirmar_senha:
            flash("As senhas não coincidem!", "error")
            return render_template('cadastrar_usuarios.html')
        sucesso = cadastrar_usuario_model(usuario, cargo, senha)

        if sucesso:
            flash('✅ Usuário cadastrado com sucesso! 😊', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('⚠️ Usuário já cadastrado!', 'error')
        return render_template('cadastrar_usuarios.html')
    return render_template('cadastrar_usuarios.html')
        


@auth.route('/registrar',methods=["GET", "POST"]) 
def registrar():
    if request.method == 'POST':
       
        usuario = request.form['usuario'].strip()
        senha = request.form['senha'].strip()
        confirmar_senha = request.form['confirmar_senha'].strip()
        #sanitização de acessos
        usuario = bleach.clean(usuario)
        senha = senha
        confirmar_senha = confirmar_senha

        if not usuario or not senha or not confirmar_senha:
                flash("😒 Por favor preencha todos os campos!", "error")
                return render_template('registrar.html')

        if len(senha) < 6:
            flash("A senha deve ter pelo menos 6 caracteres.", "error")
            return render_template('registrar.html')

        if senha != confirmar_senha:
            flash("As senhas não coincidem!", "error")
            return render_template('registrar.html')
        sucesso =registrar_usuario(usuario, senha)

        if sucesso:
            flash('✅ Usuário registrado com sucesso! 😊', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('⚠️ Usuário já registrado!', 'error')
        return render_template('registrar.html')
    return render_template('registrar.html')
        
@auth.route('/login_painel',methods=['GET', 'POST'])
def login_painel():
    if request.method =='POST': 
        usuario_input = bleach.clean(request.form['usuario'])
        senha = request.form['senha'].strip()
        if 'login_attempts' not in session:
            session['login_attempts'] = 0
            session['lockout_time'] = None

        if session.get('lockout_time') and time.time() < session['lockout_time']:
            flash("Você excedeu o numero de tentativas. Tente novamente em alguns minutos.", "error")
            return redirect(url_for('auth.login_painel'))

        if not usuario_input or not senha:
            flash("😒 Por favor preencha todos os campos", "error")
            return render_template('login_painel.html')  # interrompe execução aqui

        usuario = autenticar_usuario(usuario_input, senha)

        if usuario:
            session['usuario'] = {'nome': usuario.get('nome') or usuario.get('usuario'),
                                '_id': str(usuario.get('_id'))}
            login_user(User(usuario))
            session['login_attempts'] = 0  # Zera tentativas
            session['lockout_time'] = None
            flash('✅ Login realizado com sucesso! 😊😊', 'success')
            return redirect(url_for('auth.painel_view'))
        else:
            session['login_attempts'] += 1
            if session['login_attempts'] >= MAX_LOGIN_ATTEMPTS:
                session['lockout_time'] = time.time() + LOCKOUT_TIME
                flash("🚫 Muitas tentativas. Tente novamente em 5 minutos.", 'error')
            else:
                flash('😭 Usuário ou senha incorretos!', 'error')
            return render_template('login_painel.html')

    return render_template('login_painel.html')

@auth.route('/login',methods=['GET', 'POST'])
def login():
    if request.method =='POST': 
        usuario_input = bleach.clean(request.form['usuario'])
        senha = request.form['senha'].strip()
        if 'login_attempts' not in session:
            session['login_attempts'] = 0
            session['lockout_time'] = None

        if session.get('lockout_time') and time.time() < session['lockout_time']:
            flash("Você excedeu o numero de tentativas. Tente novamente em alguns minutos.", "error")
            return redirect(url_for('auth.login'))

        if not usuario_input or not senha:
            flash("😒 Por favor preencha todos os campos", "error")
            return render_template('login.html')  # interrompe execução aqui

        usuario = autenticar_usuario(usuario_input, senha)

        if usuario:
            session['usuario'] = {'nome': usuario.get('nome') or usuario.get('usuario'),
                                '_id': str(usuario.get('_id'))}
            login_user(User(usuario))
            session['login_attempts'] = 0  # Zera tentativas
            session['lockout_time'] = None
            flash('✅ Login realizado com sucesso! 😊😊', 'success')
            return redirect(url_for('main.home'))
        else:
            session['login_attempts'] += 1
            if session['login_attempts'] >= MAX_LOGIN_ATTEMPTS:
                session['lockout_time'] = time.time() + LOCKOUT_TIME
                flash("🚫 Muitas tentativas. Tente novamente em 5 minutos.", 'error')
            else:
                flash('😭 Usuário ou senha incorretos!', 'error')
            return render_template('login.html')

    return render_template('login.html')


       
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    flash("🔒 Logout realizado com sucesso.", 'success')
    return redirect(url_for('auth.login'))

@auth.route('/logout_painel')
@login_required
def logout_painel():
    logout_user()
    session.clear()
    flash("🔒 Logout realizado com sucesso.", 'success')
    return redirect(url_for('auth.login_painel'))
@auth.route('/painel')
@login_required
def painel_view():
    if 'usuario' not in session: 
        flash('😭😭😭 Você precisa estar logado!','error')
        return redirect(url_for('auth.login'))
    nome_usuario = session['usuario']['nome']
    usuarios = buscar_usuarios()  # pega lista de usuários
    
    projetos = ProjetoService.listar_todos_projetos()
    oportunidades = crm_service.listar_oportunidades() # função importada da outra rota
    return render_template('painel/home_painel.html', nome=nome_usuario, quantidade_usuarios=len(usuarios), projetos=projetos, oportunidades=oportunidades)


@auth.route('/painel/listar_usuarios')
@login_required

def listar_usuarios():
    usuarios = buscar_usuarios()  # nome da função que busca no banco, que você deve definir
    return render_template('painel/listar_usuarios.html', usuarios=usuarios, total=len(usuarios))
def buscar_usuarios():
     return list(db.usuarios_sistema.find({}))
