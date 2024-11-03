from flask import Flask, render_template
import os
import json
import sqlite3

from servers.mood_jar import *

app = Flask(__name__)
app.register_blueprint(mood_jar_bp)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
