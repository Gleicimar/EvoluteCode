from flask import render_template, flash, redirect, url_for
from bson import ObjectId
from datetime import datetime
from app.models.oportunidades import OportunidadeModel
from app.repositories.oportunidade_repository import (
    listar_oportunidades, buscar_oportunidade, atualizar_oportunidade, deletar_oportunidade, atualizar_followup, adicionar_followup, remover_followup
)

def cadastrar_oportunidade_service(req):
    if req.method == 'POST':
        oportunidade = OportunidadeModel(
            nome=req.form.get("nome"),
            email=req.form.get("email"),
            telefone=req.form.get("telefone"),
            projeto=req.form.get("projeto"),
            origem=req.form.get("origem", "site"),
            status=req.form.get("status", "novo"),
            followup=[],
            data=datetime.utcnow()
        )
        oportunidade.salvar()
        flash("Solicitação cadastrada com sucesso!", "success")
    return render_template("cadastrar_oportunidade.html")

def listar_oportunidades_service():
    return listar_oportunidades()

def editar_oportunidade_service(id, req):
    oportunidade = buscar_oportunidade(id)
    if req.method == 'POST':
        dados = {
            'nome': req.form['nome'],
            'email': req.form['email'],
            'telefone': req.form.get('telefone', ''),
            'projeto': req.form.get('projeto', ''),
            'origem': req.form.get('origem', ''),
            'status': req.form.get('status', 'novo'),
            'observacao': req.form.get('observacao', '')
        }
        atualizar_oportunidade(id, dados)
        flash('Oportunidade atualizada com sucesso!', 'success')
        return redirect(url_for('crm.route_listar_oportunidades'))
    return render_template('editar_oportunidades.html', oportunidade=oportunidade)

def deletar_oportunidade_service(id):
    sucesso = deletar_oportunidade(id)
    if sucesso:
        flash('Oportunidade excluída com sucesso!', 'success')
    else:
        flash('Oportunidade não encontrada.', 'error')
    return redirect(url_for('crm.route_listar_oportunidades'))

def visualizar_detalhes_service(id, req, session):
    oportunidade = buscar_oportunidade(id)
    if not oportunidade:
        flash("Ah não 🥹! Oportunidade não encontrada!")
        return redirect(url_for('crm.route_listar_oportunidades'))

    excluir_id = req.args.get('excluir_followup_id')
    if excluir_id:
        remover_followup(id, excluir_id)
        flash("❌ Follow-up excluído com sucesso.", "success")
        return redirect(url_for('crm.route_detalhes', id=id))

    if req.method == 'POST':
        from app.utils.followup_utils import handle_followup_post
        return handle_followup_post(id, req, session)

    editar_followup_id = req.args.get('editar_followup_id')
    followup_para_editar = next(
        (f for f in oportunidade.get('followup', []) if str(f.get('_id')) == editar_followup_id), None)

    return render_template("detalhes_oportunidade.html",
                           oportunidade=oportunidade,
                           followup_para_editar=followup_para_editar)
