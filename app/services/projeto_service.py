from flask import flash, redirect, url_for
from app.utils.imagem_utils import salvar_imagem, deletar_imagem
from app.repositories.projeto_repository import (
    inserir_projeto,
    listar_projetos,
    buscar_projeto,
    remover_projeto,
    atualizar_projeto
)
import datetime

class ProjetoService:
    @staticmethod
    def cadastrar_projeto(req):
        nome_empresa = req.form.get('nome_empresa', '').strip()
        tecnologia = req.form.get('tecnologia', '').strip()
        descricao = req.form.get('descricao', '').strip()
        imagem = req.files.get('imagem')

        if not nome_empresa or not tecnologia or not descricao or not imagem or not imagem.filename:
            flash('Preencha todos os campos obrigatórios.', 'error')
            return redirect(req.url)

        imagem_id = salvar_imagem(imagem)
        projeto = {
            'nome_empresa': nome_empresa,
            'tecnologia': tecnologia,
            'descricao': descricao,
            'imagem_id': imagem_id,
            'data': datetime.datetime.now()
        }
        inserir_projeto(projeto)
        flash('Projeto cadastrado com sucesso!', 'success')
        return redirect(url_for('projetos_auth.route_listar_projetos'))

    @staticmethod
    def listar_todos_projetos():
        return listar_projetos()

    @staticmethod
    def buscar_projeto_por_id(projeto_id):
        return buscar_projeto(projeto_id)

    @staticmethod
    def editar_projeto(projeto_id, req):
        projeto = buscar_projeto(projeto_id)
        if not projeto:
            flash('Projeto não encontrado.', 'error')
            return redirect(url_for('projetos_auth.route_listar_projetos'))

        dados = {
            'nome_empresa': req.form.get('nome_empresa'),
            'tecnologia': req.form.get('tecnologia'),
            'descricao': req.form.get('descricao'),
            'data_inicio': req.form.get('data_inicio'),
            'data_final': req.form.get('data_final')
        }

        novo_arquivo = req.files.get('imagem')
        if novo_arquivo and novo_arquivo.filename != '':
            if 'imagem_id' in projeto:
                deletar_imagem(projeto['imagem_id'])
            imagem_id = salvar_imagem(novo_arquivo)
            dados['imagem_id'] = imagem_id

        atualizar_projeto(projeto_id, dados)
        flash('Projeto atualizado com sucesso!', 'success')
        return redirect(url_for('projetos_auth.route_listar_projetos'))

    @staticmethod
    def excluir_projeto(projeto_id):
        projeto = buscar_projeto(projeto_id)
        if not projeto:
            flash('Projeto não encontrado.', 'error')
            return redirect(url_for('projetos_auth.route_listar_projetos'))

        if 'imagem_id' in projeto:
            try:
                deletar_imagem(projeto['imagem_id'])
            except Exception as e:
                flash(f'Erro ao deletar imagem: {e}', 'warning')

        remover_projeto(projeto_id)
        flash('Projeto deletado com sucesso!', 'success')
        return redirect(url_for('projetos_auth.route_listar_projetos'))
