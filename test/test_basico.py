import os
import pytest
from app import create_app
from app.models.mongo import db as mongo_db
from app.models.user_model import UserModel
from app.models.oportunidades import OportunidadeModel
from bson.objectid import ObjectId

# conftest.py
@pytest.fixture(scope='session')
def test_app():
    # Setup Flask test app
    os.environ['FLASK_ENV'] = 'testing'
    os.environ['MONGO_URI'] = 'mongodb://localhost:27017/evolutecode_test'
    app = create_app()
    app.config['TESTING'] = True

    # Ensure test database is clean
    with app.app_context():
        mongo_db.client.drop_database('evolutecode_test')

    yield app

    # Teardown: drop test database
    mongo_db.client.drop_database('evolutecode_test')

@pytest.fixture()
def client(test_app):
    return test_app.test_client()

# tests/test_user_model.py
class TestUserModel:
    def test_create_and_find_user(self, test_app):
        with test_app.app_context():
            # Create user
            user_data = {'username': 'testuser', 'email': 'test@example.com', 'password': 'password123'}
            user = UserModel(**user_data)
            inserted = mongo_db.db.users.insert_one(user.__dict__)
            assert inserted.inserted_id is not None

            # Find user
            found = UserModel.find_by_username('testuser')
            assert found is not None
            assert found['email'] == 'test@example.com'

# tests/test_oportunidade_model.py
class TestOportunidadeModel:
    def test_create_and_get_oportunidade(self, test_app):
        with test_app.app_context():
            data = {'title': 'Test Opp', 'description': 'Desc', 'created_by': 'tester'}
            opp = OportunidadeModel(**data)
            inserted = opp.save()
            assert isinstance(inserted, str)
            # Retrieve
            retrieved = OportunidadeModel.get_by_id(inserted)
            assert retrieved['_id'] == ObjectId(inserted)
            assert retrieved['title'] == 'Test Opp'

# tests/test_auth_routes.py
class TestAuthRoutes:
    def test_register_and_login(self, client):
        # Register new user
        response = client.post('/auth/register', data={
            'username': 'user1',
            'email': 'user1@example.com',
            'password': 'pass',
            'confirm_password': 'pass'
        }, follow_redirects=True)
        assert response.status_code == 200
        assert b'Registration successful' in response.data

        # Login
        response = client.post('/auth/login', data={
            'username': 'user1',
            'password': 'pass'
        }, follow_redirects=True)
        assert response.status_code == 200
        assert b'Welcome user1' in response.data

# tests/test_crm_routes.py
class TestCrmRoutes:
    def login(self, client):
        client.post('/auth/register', data={
            'username': 'crmuser',
            'email': 'crm@example.com',
            'password': 'pass',
            'confirm_password': 'pass'
        })
        return client.post('/auth/login', data={
            'username': 'crmuser',
            'password': 'pass'
        }, follow_redirects=True)

    def test_create_oportunidade(self, client):
        # Login first
        self.login(client)
        # Create opportunity
        response = client.post('/crm/cadastrar_oportunidade', data={
            'title': 'Opp1',
            'description': 'Desc1'
        }, follow_redirects=True)
        assert response.status_code == 200
        assert b'Oportunidade cadastrada' in response.data

    def test_list_oportunidades(self, client):
        self.login(client)
        response = client.get('/crm/oportunidades')
        assert response.status_code == 200
        assert b'Oportunidades Cadastradas' in response.data

    def test_delete_oportunidade(self, client):
        self.login(client)
        # Create then delete
        post = client.post('/crm/cadastrar_oportunidade', data={'title': 'ToDelete', 'description': 'X'})
        # extract id from redirect or page; here we simulate retrieval
        with client.application.app_context():
            opp = mongo_db.db.oportunidades.find_one({'title': 'ToDelete'})
            oid = str(opp['_id'])
        response = client.get(f'/crm/excluir_oportunidade/{oid}', follow_redirects=True)
        assert response.status_code == 200
        assert b'Oportunidade excluida' in response.data

# To run: pytest tests/ --maxfail=1 --disable-warnings -q
