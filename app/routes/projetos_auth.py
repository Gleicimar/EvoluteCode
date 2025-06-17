from passlib.hash import bcrypt
from flask import Blueprint, render_template, request, flash, get_flashed_messages,redirect, session, url_for
from flask_login import UserMixin, login_user, login_required

from flask import flash
from werkzeug.utils import secure_filename
from app.models.mongo import db, fs
import datetime

projetos_auth = Blueprint('projetos_auth', __name__)

@projetos_auth.route('/painel/cadastrar_projetos',methods=['GET', 'POST'])
@login_required   
def cadastrar_projetos():
        nome_empresa = request.form.get('nome_empresa','').split()
        tecnologia = request.form.get('tecnologia','').split()
        descricao = request.form.get('descricao','').split()
        imagem = request.files.get('imagem')

        if imagem:
            imagem_id = fs.put(imagem, filename=secure_filename(imagem.filename))
        else:
            imagem_id = None

            db.projetos.insert_one({
            'nome_empresa' : nome_empresa,
            'tecnologia' :tecnologia,
            'descricao' :descricao,
            'imagem_id' :imagem_id,
            'data':datetime.datetime.now()})

        return render_template('cadastrar_projetos.html') 


     