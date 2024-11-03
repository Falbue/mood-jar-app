from flask import Flask, render_template
import os
import json
import sqlite3

app = Flask(__name__)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # текущая директория скрипта
# SCRIPT_DIR = os.path.dirname(PARENT_DIR)  # директория уровнем выше
print(os.path.dirname(os.path.dirname(SCRIPT_DIR)))
DB_HUB = os.path.join(os.path.dirname(os.path.dirname(SCRIPT_DIR)), 'db_hub')
DB_HUB = SCRIPT_DIR if not (os.path.exists(DB_HUB) and os.path.isdir(DB_HUB)) else DB_HUB
DB_NAME = 'mood_jar.db'
DB_PATH = f"{DB_HUB}/{DB_NAME}"
VERSION = "aplha"

def now_time():  # Получение текущего времени по МСК
    now = datetime.now()
    tz = pytz.timezone('Europe/Moscow')
    now_moscow = now.astimezone(tz)
    current_time = now_moscow.strftime("%H:%M:%S")
    current_date = now_moscow.strftime("%Y.%m.%d")
    return current_date, current_time

def SQL_request(request, params=()):  # Выполнение SQL-запросов
    connect = sqlite3.connect(DB_PATH)
    cursor = connect.cursor()
    if request.strip().lower().startswith('select'):
        cursor.execute(request, params)
        result = cursor.fetchone()
        connect.close()
        return result
    else:
        cursor.execute(request, params)
        connect.commit()
        connect.close()

def get_files(directory, extensions):
    file_list = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(tuple(extensions)):
                file_list.append(os.path.relpath(os.path.join(root, file), directory))
    return file_list

@app.context_processor
def inject_files():
    css_directory = os.path.join(app.static_folder, 'styles')
    js_directory = os.path.join(app.static_folder, 'scripts')
    css_files = get_files(css_directory, ['.css'])
    js_files = get_files(js_directory, ['.js'])
    return dict(css_files=css_files, js_files=js_files)

@app.route('/')
def index():
    return render_template('placeholder.html')
    

@app.route('/jar/<int:user_id>')
def jar(user_id):
    user = SQL_request("SELECT * FROM users WHERE id = ?", (user_id,))
    jar = json.loads(user[6])
    return render_template('jar.html', jar=jar)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)