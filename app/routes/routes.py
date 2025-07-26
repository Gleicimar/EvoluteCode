from flask import Blueprint, flash, render_template, request, get_flashed_messages,redirect, session, url_for
from flask_login import login_user, logout_user, login_required, current_user
from app import login_manager
from datetime import datetime, timedelta

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html', messages=get_flashed_messages(),usuario=current_user )


