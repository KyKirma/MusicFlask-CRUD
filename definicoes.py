import os
from musica import app

def recupera_imagem(id):
    for imagem in os.listdir(app.config['UPLOAD_PASTA']):
        ext = str(imagem).split('.')

        if ext[0] == f'album{id}':
            return imagem

    return 'default.png'