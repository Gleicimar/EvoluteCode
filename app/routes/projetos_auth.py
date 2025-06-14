from passlib.hash import bcrypt
from flask import Blueprint, render_template, request, flash, get_flashed_messages,redirect, session, url_for
from flask_login import UserMixin
from flask import flash
from werkzeug.utils import secure_filename
from app.models.mongo import db
import datetime

projetos_auth = Blueprint('projetos_auth', __name__)

@projetos_auth.route('/painel/cadastrar_projetos',methods=['GET', 'POST'])
@login_required   
def cadastrar_projetos():
        nome = request.form['nome_empresa']
        tecnologia = request.form['tecnologia']
        descricao = request.form['descricao']
        imagem = request.files['imagem']

        if imagem:
            imagem_id = fs.put(imagem, filename=secure_filename(imagem.filename))
        else:
            imagem_id = None

        mongo.db.projetos.insert_one({
            'nome' : nome,
            'tecnologia' :tecnologia,
            'descricao' :descricao,
            'imagem_id' :imagem_id,
            'data':datetime.datetime.now()})

        return redirect(url_for('cadastrar_projetos'))


     