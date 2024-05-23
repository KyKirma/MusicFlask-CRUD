from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pip

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

from views import *

if __name__ == '__main__':
    try:
        pip.main(['install', '-r', 'requirements.txt'])
    except Exception as e:
        print(f"Erro ao instalar pacotes: {e}")
    finally:
        app.run(debug = True)