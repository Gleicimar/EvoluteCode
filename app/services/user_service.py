from app.repositories.user_repository import listar_todos_usuarios

class UserService:
    def listar_usuarios(self):
        return listar_todos_usuarios()
