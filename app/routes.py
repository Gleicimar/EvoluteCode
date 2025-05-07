from flask import Blueprint, flash, render_template, request, flash, get_flashed_messages

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')
@main.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username= request.form['usuario']
        password = request.form['senha']
        if username =="admin" or password =="admin":
            flash('Usuario ou senha incorretos')
            return render_template('login.html')
        flash('Login efetuado com sucesso')
        return render_template('home.html')
    return render_template('login.html')