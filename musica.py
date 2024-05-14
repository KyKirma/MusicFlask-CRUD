from flask import Flask, render_template, request, redirect

class Musica:
    def __init__(self, nome, banda, genero):
        self.nome = nome
        self.banda = banda
        self.genero = genero

musica01 = Musica('Tell Me You Know', 'Good Kid', 'Rock Alt')
musica02 = Musica('Todo Mundo Menos Você', 'Marília Mendonça', 'Sertanejo')
musica03 = Musica('My Love Mine All Mine', 'Mitski', 'Alternativo')
musica04 = Musica('Apesar de Você', 'Chico Buearque', 'MPB')
lista = [musica01, musica02, musica03, musica04]

app = Flask(__name__)

@app.route('/')
def listarMusicas():
    return render_template('lista_musicas.html', 
                           titulo = 'Aprendendo',
                           musicas = lista)

@app.route('/cadmusicas')
def cadastrarMusica():
    return render_template('cadastra_musica.html')

@app.route('/add', methods = ['POST',])
def adicionarMusica():
    nome = request.form['txtNomeMusica']
    banda = request.form['txtBanda']
    genero = request.form['txtGenero']

    lista.append(Musica(nome, banda, genero))

    return redirect('/')

app.run(debug = True)