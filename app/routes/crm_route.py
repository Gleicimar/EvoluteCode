from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_required
from app.services.oportunidade_service import (
    cadastrar_oportunidade_service,
    listar_oportunidades_service,
    editar_oportunidade_service,
    deletar_oportunidade_service,
    visualizar_detalhes_service
)

crm = Blueprint('crm', __name__)

@crm.route('/cadastrar_oportunidade', methods=['GET', 'POST'])
def route_cadastrar_oportunidade():
    return cadastrar_oportunidade_service(request)

@crm.route('/listar_oportunidades')
@login_required
def route_listar_oportunidades():
    oportunidades = listar_oportunidades_service()
    return render_template("listar_oportunidades.html", oportunidades=oportunidades)

@crm.route('/editar_oportunidades/<id>', methods=['GET', 'POST'])
@login_required
def route_editar_oportunidade(id):
    return editar_oportunidade_service(id, request)

@crm.route('/deletar/<id>', methods=['GET'])
@login_required
def route_deletar(id):
    return deletar_oportunidade_service(id)

@crm.route('/detalhes_oportunidades/<id>', methods=['GET', 'POST'])
@login_required
def route_detalhes(id):
    return visualizar_detalhes_service(id, request, session)
