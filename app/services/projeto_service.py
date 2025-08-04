# services/projeto_service.py (refatorado para separar lógica de negócio e controle HTTP)
from bson.objectid import ObjectId

from flask import Response

from app.models.mongo import db, fs

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
    def validar_dados_projeto(form, imagem_required=True):
        nome_empresa = form.get('nome_empresa', '').strip()
        tecnologia = form.get('tecnologia', '').strip()
        descricao = form.get('descricao', '').strip()

        if not nome_empresa or not tecnologia or not descricao:
            return False, 'Preencha todos os campos obrigatórios.'

        if imagem_required:
            imagem = form.get('imagem')
            if not imagem or not imagem.filename:
                return False, 'Imagem obrigatória.'

        return True, ''

    @staticmethod
    def montar_dados_projeto(form, imagem_file=None, imagem_antiga_id=None):
        dados = {
            'nome_empresa': form.get('nome_empresa').strip(),
            'tecnologia': form.get('tecnologia').strip(),
            'descricao': form.get('descricao').strip(),
            'data': datetime.datetime.now()
        }

        if imagem_file and imagem_file.filename:
            if imagem_antiga_id:
                deletar_imagem(imagem_antiga_id)
            imagem_id = salvar_imagem(imagem_file)
            dados['imagem_id'] = imagem_id

        return dados

    @staticmethod
    def cadastrar_projeto_service(form, imagem_file):
        dados = ProjetoService.montar_dados_projeto(form, imagem_file)
        inserir_projeto(dados)

    @staticmethod
    def listar_todos_projetos():
        return listar_projetos()

    @staticmethod
    def buscar_projeto_por_id(projeto_id):
        return buscar_projeto(projeto_id)

    @staticmethod
    def editar_projeto_service(projeto_id, form, imagem_file):
        projeto = buscar_projeto(projeto_id)
        if not projeto:
            return None
        dados = ProjetoService.montar_dados_projeto(form, imagem_file, projeto.get('imagem_id'))
        atualizar_projeto(projeto_id, dados)
        return True

    @staticmethod
    def deletar_projeto_service(projeto_id):
        projeto = buscar_projeto(projeto_id)
        if not projeto:
            return None
        if 'imagem_id' in projeto:
            deletar_imagem(projeto['imagem_id'])
        remover_projeto(projeto_id)
        return True

    @staticmethod
    
    def exibir_imagem_service(imagem_id):
        try:
            imagem = fs.get(ObjectId(imagem_id))
            return Response(imagem.read(), mimetype=imagem.content_type)
        except Exception as e:
            return Response(f"Erro ao carregar imagem: {str(e)}", status=404)