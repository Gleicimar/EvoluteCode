# app/schemas/oportunidade_schema.py

def validar_oportunidade(dados):
    erros = []
    if not dados.get("titulo"):
        erros.append("Campo 'titulo' é obrigatório.")
    if not dados.get("descricao"):
        erros.append("Campo 'descricao' é obrigatório.")
    # Adicione aqui outras regras de validação específicas
    return erros
