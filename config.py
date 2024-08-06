import os

SECRET_KEY = 'segredo'

SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql',
        usuario = 'root',
        senha = '',
        servidor = 'localhost',
        database = 'playmusica'
    )


UPLOAD_PASTA = os.path.dirname(os.path.abspath(__file__)) + '/uploads'