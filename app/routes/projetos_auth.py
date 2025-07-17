from bson import ObjectId
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from werkzeug.utils import secure_filename
from app.models.mongo import db, fs
import datetime

projetos_auth = Blueprint('projetos_auth', __name__)

@projetos_auth.route('/painel/cadastrar_projetos', methods=['GET', 'POST'])
@login_required
def cadastrar_projetos():
    if request.method == 'POST':
        nome_empresa = request.form.get('nome_empresa', '').strip()
        tecnologia = request.form.get('tecnologia', '').strip()
        descricao = request.form.get('descricao', '').strip()
        imagem = request.files.get('imagem')

        # Validação: verificar se todos os campos obrigatórios estão preenchidos
        if not nome_empresa or not tecnologia or not descricao or not imagem or not imagem.filename:
            flash('Preencha todos os campos obrigatórios.', 'error')
            return redirect(request.url)  # redireciona para o mesmo formulário

        # Processar e salvar a imagem
        imagem_id = fs.put(imagem, filename=secure_filename(imagem.filename))

        # Inserir no banco
        db.projetos.insert_one({
            'nome_empresa': nome_empresa,
            'tecnologia': tecnologia,
            'descricao': descricao,
            'imagem_id': imagem_id,
            'data': datetime.datetime.now()
        })

        flash('Projeto cadastrado com sucesso!', 'success')
        return redirect(url_for('projetos_auth.listar_projetos'))

    return render_template('cadastrar_projetos.html')



# ✅ Listagem dos projetos
@projetos_auth.route('/painel/consultar_projetos')
@login_required
def listar_projetos():
    projetos_list = list(db.projetos.find({}))
  
    return render_template('consultar_projetos.html', projetos=projetos_list )

# ✅ Exibir imagem via GridFS
@projetos_auth.route('/imagem/<imagem_id>')
def exibir_imagem(imagem_id):
    from flask import Response
    imagem = fs.get(ObjectId(imagem_id))
    return Response(imagem.read(), mimetype='image/jpeg')  # ajuste se for png

# ⚠️ Ajuste: Essa função abaixo está errada (estava misturando HTML dentro da função).
# Deixe a função de atualização separada com rota futura.
