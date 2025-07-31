from flask import Blueprint, render_template, request, redirect, url_for, flash, Response
from flask_login import login_required
from bson import ObjectId
from app.services.projeto_service import ProjetoService
from app.utils.imagem_utils import buscar_imagem

projetos_auth = Blueprint('projetos_auth', __name__)

@projetos_auth.route('/painel/cadastrar_projetos', methods=['GET', 'POST'])
@login_required
def route_cadastrar_projetos():
    if request.method == 'POST':
        return ProjetoService.cadastrar_projeto(request) 
    return render_template('cadastrar_projetos.html')

@projetos_auth.route('/painel/consultar_projetos')
@login_required
def route_listar_projetos():
    projetos = ProjetoService.listar_todos_projetos()
    return render_template('consultar_projetos.html', projetos=projetos)

@projetos_auth.route('/imagem/<imagem_id>')
def route_exibir_imagem(imagem_id):
    imagem = buscar_imagem(imagem_id)
    return Response(imagem.read(), mimetype='image/jpeg')

@projetos_auth.route('/painel/deletar_projetos/<projeto_id>')
def route_deletar_projeto(projeto_id):
    return ProjetoService.excluir_projeto(projeto_id)

@projetos_auth.route('/painel/editar_projetos/<projeto_id>', methods=['GET', 'POST'])
def route_editar_projeto(projeto_id):
    if request.method == 'POST':
        return ProjetoService.editar_projeto(projeto_id, request)
    projeto = ProjetoService.buscar_projeto_por_id(projeto_id)
    return render_template('editar_projetos.html', projeto=projeto)
