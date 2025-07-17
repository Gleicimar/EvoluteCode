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
    print(f"Total de projetos encontrados: {len(projetos_list)}") 
    return render_template('consultar_projetos.html', projetos=projetos_list )
def buscar_todos_projetos():
    projetos_list = list(db.projetos.find({}))
    print(f"Total de projetos encontrados: {len(projetos_list)}") 
    return projetos_list

# ✅ Exibir imagem via GridFS
@projetos_auth.route('/imagem/<imagem_id>')
def exibir_imagem(imagem_id):
    from flask import Response
    imagem = fs.get(ObjectId(imagem_id))
    return Response(imagem.read(), mimetype='image/jpeg')  # ajuste se for png

# ⚠️ Ajuste: Essa função abaixo está errada (estava misturando HTML dentro da função).
# Deixe a função de atualização separada com rota futura.

@projetos_auth.route('/painel/deletar_projetos/<projeto_id>')
def deletar_projeto(projeto_id):
    try:
        projeto = db.projetos.find_one({'_id': ObjectId(projeto_id)})

        if not projeto:
            flash('Projeto não encontrado.', 'error')
            return redirect(url_for('projetos_auth.listar_projetos'))

        # Deleta a imagem no GridFS usando o imagem_id
        if 'imagem_id' in projeto:
            try:
                imagem_id = ObjectId(projeto['imagem_id'])
                fs.delete(imagem_id)
            except Exception as e:
                flash(f'Erro ao deletar a imagem no GridFS: {e}', 'warning')

        # Deleta o projeto do banco
        db.projetos.delete_one({'_id': ObjectId(projeto_id)})

        flash('Projeto deletado com sucesso!', 'success')
    except Exception as e:
        flash(f'Ocorreu um erro ao deletar o projeto: {e}', 'error')

    return redirect(url_for('projetos_auth.listar_projetos'))
@projetos_auth.route('/painel/editar_projetos/<projeto_id>',methods=['GET', 'POST'])
def editar_projetos(projeto_id):
    projeto=db.projetos.find_one({'_id': ObjectId(projeto_id)})
    if not projeto:
        flash('Projeto não encontrado.', 'error')
        return redirect(url_for('projetos_auth.listar_projetos'))

    if request.method=='POST':
        nome_empresa = request.form.get('nome_empresa')
        tecnologia = request.form.get('tecnologia')
        descricao = request.form.get('descricao')
        novo_arquivo = request.files.get('imagem')
        data_inicio = request.form.get('data_inicio')
        data_final = request.form.get('data_final')
        
         # Atualiza campos básicos
        update_data = {
            'nome_empresa': nome_empresa,
            'tecnologia': tecnologia,
            'descrição': descricao,
            'data_inicio': data_inicio,
            'data_final': data_final,
        }
        # Substitui a imagem no GridFS, se for enviada uma nova
        if novo_arquivo and novo_arquivo.filename != '':
                try:
                    # Deleta a imagem antiga, se existir
                    if 'imagem_id' in projeto:
                        fs.delete(ObjectId(projeto['imagem_id']))

                    # Salva nova imagem
                    imagem_id = fs.put(novo_arquivo, filename=novo_arquivo.filename, content_type=novo_arquivo.content_type)
                    update_data['imagem_id'] = imagem_id
                except Exception as e:
                    flash(f'Erro ao atualizar a imagem: {e}', 'warning')
             # Atualiza no banco
        db.projetos.update_one({'_id': ObjectId(projeto_id)}, {'$set': update_data})
        flash('Projeto atualizado com sucesso!', 'success')
        return redirect(url_for('projetos_auth.listar_projetos'))

    # GET: exibe o formulário preenchido
    return render_template('editar_projetos.html', projeto=projeto)