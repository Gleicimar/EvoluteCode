from passlib.hash import bcrypt
from flask_login import UserMixin
from flask import flash
from .mongo import db


def allowed_file(filename):
    return '.' in filename and 
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




    
    
def cadastrar_projetos(imagem, tecnologia, nome_empresa , descricao):
        file = request.files['imagem']
            if file.filename =='':
                flash('Nenhuma imagem selecionada', 'error')
                return request_url()
            file =request.files['imagem']

            if file.filename=='':
                flash('Nenhuma imagem selecionada')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename= secure_filename(file.filename)
                path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(path)
        tecnologia = request.form['tecnologia']
        nome_empresa =request.form['nome_empresa']
        data_inicio = request.form['data_inicio']
        descricao =request.form['descricao']

     