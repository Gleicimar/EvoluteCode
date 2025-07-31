from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from app.repositories.user_repository import buscar_usuario_por_nome, criar_usuario

class AuthService:
    def authenticate_user(self, username, password):
        usuario = buscar_usuario_por_nome(username)
        if not usuario:
            return False, None, "Usuário não encontrado."

        if not check_password_hash(usuario['senha'], password):
            return False, None, "Senha incorreta."

        session['usuario'] = {'nome': usuario['usuario'], 'cargo': usuario.get('cargo', '')}
        return True, usuario, "Login realizado com sucesso!"

    def register_user(self, username, password, confirm_password, cargo='usuário'):
        if not username or not password or not confirm_password:
            return False, "Preencha todos os campos."

        if len(password) < 6:
            return False, "A senha deve ter pelo menos 6 caracteres."

        if password != confirm_password:
            return False, "As senhas não coincidem."

        sucesso = criar_usuario(username, password, cargo)
        if not sucesso:
            return False, "Usuário já existente."
        
        return True, "Usuário cadastrado com sucesso!"
