from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from bson import ObjectId

from app.services.projeto_service import ProjetoService

projetos_auth = Blueprint('projetos_auth', __name__)

@projetos_auth.route('/painel/cadastrar_projetos', methods=['GET', 'POST'])
@login_required
def route_cadastrar_projetos():
    if request.method == 'POST':
        form_data = request.form
        imagem = request.files['imagem']
        ProjetoService.cadastrar_projeto_service(request.form, request.files.get('imagem'))
        flash('Projeto cadastrado com sucesso!', 'success')
        return redirect(url_for('auth.painel_view'))
    return render_template('painel/cadastrar_projetos.html')

@projetos_auth.route('/painel/listar_projetos')
@login_required
def route_listar_projetos():
    projetos = ProjetoService.listar_todos_projetos()
    return render_template('painel/listar_projetos.html', projetos=projetos)

@projetos_auth.route('/imagem/<imagem_id>')
@login_required
def route_exibir_imagem(imagem_id):
    return ProjetoService.exibir_imagem_service(imagem_id)

@projetos_auth.route('/painel/editar_projeto/<projeto_id>', methods=['GET', 'POST'])
@login_required
def route_editar_projeto(projeto_id):
    if request.method == 'POST':
        form_data = request.form
        imagem = request.files.get('imagem')
        ProjetoService.editar_projeto_service(projeto_id, form_data, imagem)
        flash('Projeto editado com sucesso!', 'success')
        return redirect(url_for('projetos_auth.route_listar_projetos'))

    projeto = ProjetoService.buscar_projeto_por_id(projeto_id)
    return render_template('painel/editar_projetos.html', projeto=projeto) 

@projetos_auth.route('/painel/deletar_projeto/<projeto_id>', methods=['POST', 'GET'])
@login_required
def route_deletar_projeto(projeto_id):
    ProjetoService.deletar_projeto_service(projeto_id)
    flash('Projeto excluído com sucesso!', 'success')
    return redirect(url_for('projetos_auth.route_listar_projetos'))  