from flask import flash, redirect, url_for
from bson import ObjectId
from datetime import datetime
from app.repositories.oportunidade_repository import atualizar_followup, adicionar_followup

def handle_followup_post(id, req, session):
    descricao = req.form.get('followup')
    followup_id = req.form.get('followup_id')
    autor = session.get('usuario', {}).get('nome', 'Desconhecido')
    data = datetime.now().strftime('%d/%m/%Y %H:%M')

    if followup_id:
        atualizar_followup(id, followup_id, descricao, autor, data)
        flash("✅ Follow-up atualizado com sucesso.", "success")
    else:
        novo_followup = {
            '_id': ObjectId(),
            'descricao': descricao,
            'autor': autor,
            'data': data
        }
        adicionar_followup(id, novo_followup)
        flash("✅ Novo follow-up salvo.", "success")

    return redirect(url_for('crm.route_detalhes', id=id))
