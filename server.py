
from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify, flash, send_from_directory, jsonify
import sqlite3
import os
import random
import hashlib
from app_modules.scripts import *


app = Flask(__name__)

def get_files(directory, extensions):
    file_list = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(tuple(extensions)):
                file_list.append(os.path.relpath(os.path.join(root, file), directory))
    return file_list

@app.context_processor
def inject_files():
    css_directory = os.path.join(app.static_folder, 'css')
    js_directory = os.path.join(app.static_folder, 'js')
    
    css_files = get_files(css_directory, ['.css'])
    js_files = get_files(js_directory, ['.js'])
    
    return dict(css_files=css_files, js_files=js_files)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        hashed_password = hashlib.sha256(password.encode()).hexdigest()  # Хешируем пароль для безопасности

        user = SQL_request('SELECT * FROM users WHERE email = ?', (email,))

        if user:
            # Если пользователь существует, проверяем пароль
            if user[12] == hashed_password:
                resp = make_response(redirect(url_for('index')))
                resp.set_cookie('user', user[4])
                return resp
            else:
                return "Неверный пароль", 400
        else:
            date, time = now_time()
            date = f"{date} {time}"
            # Если пользователя нет, создаем новый
            SQL_request('INSERT INTO users (email, password, time_registration, auth_method) VALUES (?, ?, ?, ?)',
                (email, hashed_password, "email", date))

            # Создаем куку для регистрации
            resp = make_response(redirect(url_for('index')))
            resp.set_cookie('registration', email)
            return resp

    if request.method == 'GET':
        user_cookie = request.cookies.get('user')
        username_cookie = request.cookies.get('registration')
    
        if user_cookie:
            # Если кука есть, просто рендерим страницу
            return render_template('index.html', user=user_cookie)
        elif username_cookie:
            return render_template('index.html', message='username')
        else:
            # Если куки нет, выводим сообщение
            return render_template('index.html', message='registration')

@app.route('/logout')
def logout():
    resp = make_response(redirect(url_for('index')))
    resp.set_cookie('user', '', expires=0)
    return resp

@app.route('/username', methods=['POST'])
def username():
    username = request.form['username']
    user_email = request.cookies.get('registration')

    # Проверка на наличие такого же имени пользователя
    existing_user = SQL_request('SELECT * FROM users WHERE username = ?', (username,))
    
    if existing_user:  # Если имя пользователя уже существует
        # Возвращаем ошибку или сообщение
        return "Username already taken, please choose another one.", 400  # Пример возврата ошибки с кодом 400

    # Обновляем имя пользователя
    SQL_request("UPDATE users SET username = ? WHERE email = ?", (username, user_email))

    # Получаем данные о пользователе
    user = SQL_request('SELECT * FROM users WHERE email = ?', (user_email,))

    # Создаем ответ с редиректом
    resp = make_response(redirect(url_for('index')))
    resp.set_cookie('registration', '', expires=0)
    resp.set_cookie('user', user[4])  # Возможно, вы хотите сохранить какой-то параметр из 'user', например, id или имя

    return resp

app.run(host='0.0.0.0', port=80)