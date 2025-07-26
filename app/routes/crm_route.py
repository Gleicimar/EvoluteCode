from flask import Blueprint, render_template, request, flash, redirect, url_for
from bson import ObjectId
from datetime import datetime
from app.models.oportunidades import OportunidadeModel  # certifique-se de que está correto
from flask_login import login_required
from app.models.mongo import db

crm = Blueprint('crm', __name__)

@crm.route('/cadastrar_oportunidade', methods =['GET', 'POST'])
def cadastrar_oportunidade():
    if request.method == 'POST':
        nome = request.form.get("nome")
        email = request.form.get("email")
        telefone = request.form.get("telefone")
        projeto = request.form.get("projeto")  # o nome do campo no HTML é "descricao"
        origem = request.form.get("origem", "site")
        status = request.form.get("status", "novo")
        data = datetime.utcnow()
        followup = []   

        oportunidade = OportunidadeModel(
            nome = nome,
            email = email,
            telefone = telefone,
            projeto = projeto,
            origem = origem,
            status = status,
            followup = followup,
            data = data
        )

        oportunidade.salvar()
        flash("Solicitação cadastrada com sucesso!", "success")
   

    
    return render_template("cadastrar_oportunidade.html")

@crm.route('/listar_oportunidades')
@login_required
def listar_oportunidades():
    oportunidades = OportunidadeModel.listar()
    return render_template("listar_oportunidades.html", oportunidades=oportunidades)
def buscar_oportunidades():
    return list(db.oportunidades.find({}))
@crm.route('/editar_oportunidades/<id>', methods=['GET', 'POST'])
@login_required
def editar_oportunidade(id):
    oportunidade = db.oportunidades.find_one({'_id': ObjectId(id)})

    if request.method == 'POST':
        dados = {
            'nome': request.form['nome'],
            'email': request.form['email'],
            'telefone': request.form.get('telefone', ''),
            'projeto': request.form.get('projeto', ''),
            'origem': request.form.get('origem', ''),
            'status': request.form.get('status', 'novo'),
            'observacao': request.form.get('observacao', '')
        }
        db.oportunidades.update_one({'_id': ObjectId(id)}, {'$set': dados})
        flash('Oportunidade atualizada com sucesso!', 'success')
        return redirect(url_for('crm.listar_oportunidades'))

    return render_template('/editar_oportunidades.html', oportunidade=oportunidade)

@crm.route('/deletar/<id>', methods=['GET', 'POST'])
@login_required
def deletar(id):
    try:
        oportunidade = db.oportunidades.delete_one({'_id':ObjectId(id)})
        if  oportunidade.deleted_count==1:
            flash('Oportunidade excluida com sucesso!', 'success')
        else:
            flash('Oportunidade não encontrada.','error')
    except Exception as e:
            flash(f'Erro ao excluir:{e}','error')
    return redirect(url_for('crm.listar_oportunidades'))


@crm.route('/detalhes_oportunidades/<id>', methods=['GET', 'POST'])
@login_required
def visualizar_detalhes_oportunidade(id):
    oportunidade = db.oportunidades.find_one({'_id': ObjectId(id)})
    if not oportunidade:
        flash("Ah não 🥹! Oportunidade não encontrada!")
        return redirect(url_for('crm.listar_oportunidades'))
    return render_template('detalhes_oportunidade.html', oportunidade=oportunidade)