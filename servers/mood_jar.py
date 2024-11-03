from flask import Blueprint, render_template

mood_jar_bp = Blueprint('mood_jar', __name__)

@mood_jar_bp.route('/mood-jar')
def mood_jar():
    return render_template('mood_jar/mood-jar.html')








# SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # текущая директория скрипта
# # SCRIPT_DIR = os.path.dirname(PARENT_DIR)  # директория уровнем выше
# print(os.path.dirname(os.path.dirname(SCRIPT_DIR)))
# DB_HUB = os.path.join(os.path.dirname(os.path.dirname(SCRIPT_DIR)), 'db_hub')
# DB_HUB = SCRIPT_DIR if not (os.path.exists(DB_HUB) and os.path.isdir(DB_HUB)) else DB_HUB
# DB_NAME = 'mood_jar.db'
# DB_PATH = f"{DB_HUB}/{DB_NAME}"
# VERSION = "aplha"

# def SQL_request(request, params=()):  # Выполнение SQL-запросов
#     connect = sqlite3.connect(DB_PATH)
#     cursor = connect.cursor()
#     if request.strip().lower().startswith('select'):
#         cursor.execute(request, params)
#         result = cursor.fetchone()
#         connect.close()
#         return result
#     else:
#         cursor.execute(request, params)
#         connect.commit()
#         connect.close()