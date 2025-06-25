import pytest
from flask import Flask
from bson.objectid import ObjectId
from gridfs import GridFS
from io import BytesIO
from app import create_app
from app.models.mongo import db, fs  # seu acesso ao banco e ao GridFS

@pytest.fixture
def client():
    app = create_app(testing=True)  # usa banco de testes (evolutecode_test)
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            db.projetos.delete_many({})  # Limpa antes de cada teste
            if not db.usuarios.find_one({"email": "admin@teste.com"}):
                db.usuarios.insert_one({
                    "email": "admin@teste.com",
                    "senha": "admin",  # Idealmente essa senha deveria ser hash
                    "tipo": "admin"
                })
        yield client

def login(client):
    return client.post('/login', data={
        'email': 'admin@teste.com',
        'senha': 'admin'
    }, follow_redirects=True)

def test_cadastro_projeto_sem_imagem(client):
    login(client)
    response = client.post('/painel/cadastrar_projetos', data={
        'nome_empresa': 'EvoluteCode',
        'tecnologia': 'Python, Flask',
        'descricao': 'Projeto de teste'
    }, follow_redirects=True)
    assert b'Projeto cadastrado com sucesso' in response.data

def test_cadastro_projeto_com_imagem(client):
    login(client)
    data = {
        'nome_empresa': 'EvoluteCode',
        'tecnologia': 'Python, Flask',
        'descricao': 'Projeto com imagem',
        'imagem': (BytesIO(b'minhafoto'), 'teste.png')
    }
    response = client.post('/painel/cadastrar_projetos', data=data, content_type='multipart/form-data', follow_redirects=True)
    assert b'Projeto cadastrado com sucesso' in response.data

def test_listar_projetos(client):
    login(client)
    response = client.get('/listar_projetos')
    assert response.status_code == 200
    assert b'Projeto' in response.data or b'EvoluteCode' in response.data

def test_atualizar_projeto(client):
    login(client)
    db.projetos.insert_one({
        'nome_empresa': 'Teste Antigo',
        'tecnologia': 'OldTech',
        'descricao': 'Desc Antiga'
    })
    projeto = db.projetos.find_one({'nome_empresa': 'Teste Antigo'})
    response = client.post(f'/painel/atualizar_projeto/{str(projeto['_id'])}', data={
        'nome_empresa': 'Atualizado',
        'tecnologia': 'Python',
        'descricao': 'Descrição atualizada'
    }, follow_redirects=True)
    assert b'Projeto atualizado' in response.data
    projeto_atualizado = db.projetos.find_one({'_id': ObjectId(projeto['_id'])})
    assert projeto_atualizado['nome_empresa'] == 'Atualizado'

def test_cadastro_dados_invalidos(client):
    login(client)
    response = client.post('/painel/cadastrar_projetos', data={
        'nome_empresa': '',
        'tecnologia': '',
        'descricao': ''
    }, follow_redirects=True)
    assert b'campo obrigat' in response.data or response.status_code == 400
