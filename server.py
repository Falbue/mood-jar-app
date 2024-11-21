
from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify, flash, send_from_directory, jsonify
import sqlite3
import os
import random
import hashlib
import json
from app_modules.scripts import *

VERSION = '0.0.7.2'
print(VERSION)

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
                resp.set_cookie('user', user[15])
                return resp
            else:
                return "Неверный пароль", 400
        else:
            date, time = now_time()
            date = f"{date} {time}"
            mood = {"😊": "Радость", "😢": "Грусть", "😐": "Равнодушие", "😁": "Восторг", "😴": "Усталость"}
            topics = {"1": "Партнёр", "2": "Работа", "3": "Учёба", "4": "Здоровье", "5": "Друзья"}
            mood_json = json.dumps(mood, ensure_ascii=False)
            topics_json = json.dumps(topics, ensure_ascii=False)
            # Если пользователя нет, создаем новый
            SQL_request('INSERT INTO users (mood, topics, email, password, time_registration, auth_method) VALUES (?, ?, ?, ?, ? , ?)',
                (mood_json, topics_json, email, hashed_password, date, "email"))

            # Создаем куку для регистрации
            resp = make_response(redirect(url_for('index')))
            resp.set_cookie('registration', email)
            return resp

    if request.method == 'GET':
        user_cookie = request.cookies.get('user')
        username_cookie = request.cookies.get('registration')
    
        if user_cookie:
            user = SQL_request('SELECT * FROM users WHERE token = ?', (user_cookie,))
            if user is None:
                return render_template('index.html', message='registration')
            else:
                return render_template('index.html', user=user, user_moods=json.loads(user[7]))
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
    token = hashlib.sha256(username.encode()).hexdigest() 

    # Проверка на наличие такого же имени пользователя
    existing_user = SQL_request('SELECT * FROM users WHERE username = ?', (username,))
    
    if existing_user: 
        return "Username already taken, please choose another one.", 400  # Пример возврата ошибки с кодом 400

    SQL_request("UPDATE users SET username = ?, token = ? WHERE email = ?", (username, token, user_email))

    # Получаем данные о пользователе
    user = SQL_request('SELECT * FROM users WHERE email = ?', (user_email,))

    # Создаем ответ с редиректом
    resp = make_response(redirect(url_for('index')))
    resp.set_cookie('registration', '', expires=0)
    resp.set_cookie('user', user[15])

    return resp


@app.route('/get_mood_data', methods=['GET'])
def get_mood_data():
    # Получаем текущую дату в формате YYYY.MM.DD
    date, time = now_time()
    token = request.cookies.get('user')
    user = SQL_request('SELECT * FROM users WHERE token = ?', (token,))
    jar = json.loads(user[6])
    
    if date in jar:
        return jsonify(jar[date])
    else:
        print(date)
        print(json.loads(user[6]))
        return jsonify({"error": "No data for today"}), 404

@app.route('/telegram_login', methods=['POST'])
def telegram_login():
    try:
        # Извлечение данных из запроса
        data = request.get_json()
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        username = data.get('username')

        print(f"Полученные данные {first_name} {last_name} {username}")

        token = hashlib.sha256(username.encode()).hexdigest() 
        SQL_request("UPDATE users SET token = ?, WHERE username = ?", (token, username))


        resp = make_response(redirect(url_for('index')))
        resp.set_cookie('registration', '', expires=0)
        resp.set_cookie('user', token)
        return resp

    except Exception as e:
        # Обработка ошибок
        print(f"Ошибка: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


app.run(host='0.0.0.0', port=80)