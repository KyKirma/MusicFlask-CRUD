import os
from musica import app
from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField

class FormularioMusica(FlaskForm):
    nome = StringField('Nome da música', [validators.DataRequired(),
                                          validators.length(min = 2, max = 50)])
    
    grupo = StringField('Cantor / Banda / Grupo', [validators.DataRequired(),
                                                   validators.length(min = 2, max = 50)])
    
    genero = StringField('Genero', [validators.DataRequired(),
                                                   validators.length(min = 2, max = 20)])

    cadastrar = SubmitField('Cadastrar Música')
    
def recupera_imagem(id):
    for imagem in os.listdir(app.config['UPLOAD_PASTA']):
        ext = str(imagem).split('.')

        if f'album{id}_' in ext[0]:
            return imagem

    return 'default.png'

def deletar_imagem(id):
    imagem = recupera_imagem(id)

    if imagem != 'default.png':
        os.remove(os.path.join(app.config['UPLOAD_PASTA'], imagem))