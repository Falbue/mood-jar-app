from flask import Blueprint, request, jsonify
from app_modules.scripts import *
import json
import hashlib

# Создаем Blueprint для API
api_bp = Blueprint('api', __name__)

@api_bp.route('/example', methods=['GET'])
def example_route():
    return jsonify({"message": "API подключено"})

@api_bp.route('/user', methods=['POST'])
def api_user():
    data = request.get_json()
    user_id = data.get('id')
    
    if user_id is None:
        return jsonify({'status':'error', "Ошибка": "Требуется ID пользователя"}), 400

    user = SQL_request("SELECT * FROM users WHERE id = ?", (user_id,))
    
    if user:
        return jsonify({'status':'succes', "Возвращено": user})
    else:
        return jsonify({'status':'error', "Ошибка": "Пользователь не найден"}), 404

@api_bp.route('/all-data', methods=['GET'])
def api_all_data():
    data = SQL_request("SELECT * FROM users", all_data=True)
    return jsonify({"Возвращено": data})

@api_bp.route('/user/jar', methods=['POST'])
def api_jar():
    data = request.get_json()
    user_id = data.get('id')
    date = data.get('date')
    print(date)

    if user_id is None:
        return jsonify({'status':'error', "Ошибка": "Требуется ID пользователя"}), 400

    jar = SQL_request("SELECT jar FROM users WHERE id = ?", (user_id,))
    jar = json.loads(jar[0])

    if jar:
        if date:
            return jsonify({'status':'succes', f"Настроения за {date}": jar[date]})
        else:
            return jsonify({'status':'succes', "Все настроения": jar})
    else:
        return jsonify({'status':'error', "Ошибка": "Пользователь не найден"}), 404

@api_bp.route('/login', methods=['POST'])
def api_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    hashed_password = hashlib.sha256(password.encode()).hexdigest() 
    user = SQL_request('SELECT * FROM users WHERE email = ?', (email,))
    if user:
        if user[12] == hashed_password:
            token = hashlib.sha256(user[4].encode()).hexdigest() 
            SQL_request("UPDATE users SET token = ? WHERE username = ?", (token, user[4]))
            return jsonify({'status':'succes'})
        else:
            return jsonify({'status':'error', 'message':'Невеный пароль'})

    else:
        date, time = now_time()
        date = f"{date} {time}"
        mood = {"😊": "Радость", "😢": "Грусть", "😐": "Равнодушие", "😁": "Восторг", "😴": "Усталость"}
        topics = {"1": "Партнёр", "2": "Работа", "3": "Учёба", "4": "Здоровье", "5": "Друзья"}
        mood_json = json.dumps(mood, ensure_ascii=False)
        topics_json = json.dumps(topics, ensure_ascii=False)
        SQL_request('INSERT INTO users (mood, topics, email, password, time_registration, auth_method) VALUES (?, ?, ?, ?, ? , ?)',
            (mood_json, topics_json, email, hashed_password, date, "api"))

        return jsonify({'status':'succes', "message":"Зарегестрирован новый пользователь"})