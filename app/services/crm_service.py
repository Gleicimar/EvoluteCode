from app.repositories.crm_repository import listar_oportunidades, contar_por_status

class CRMService:
    def listar_oportunidades(self):
        return listar_oportunidades()

    def obter_estatisticas(self):
        return contar_por_status()
