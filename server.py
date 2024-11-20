
from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify, flash, send_from_directory, jsonify
import sqlite3
import os
import random


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
    # Получаем значение куки с именем 'user'
    user_cookie = request.cookies.get('user')

    if user_cookie:
        # Если кука есть, просто рендерим страницу
        return render_template('index.html', user=user_cookie)
    else:
        # Если куки нет, выводим сообщение
        return render_template('index.html', message="Кука 'user' отсутствует!")

app.run(host='0.0.0.0', port=80)