from flask import Blueprint, flash, render_template, request, get_flashed_messages,redirect, session, url_for
main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')


