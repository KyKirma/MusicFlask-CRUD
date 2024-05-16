from flask import Flask, render_template, request, redirect, session, flash, url_for

class Musica:
    def __init__(self, nome, banda, genero):
        self.nome = nome
        self.banda = banda
        self.genero = genero

class Usuario:
    def __init__(self, nome, login, senha):
        self.nome = nome
        self.login = login
        self.senha = senha

usuario01 = Usuario('Pedro', 'KyKirma', 'senha')
usuario02 = Usuario('Felipe', 'felps', '1234')
usuario03 = Usuario('Gustavo', 'guzin', 'pinto')

usuarios = {
    usuario01.login : usuario01,
    usuario02.login : usuario02,
    usuario03.login : usuario03
}

musica01 = Musica('Tell Me You Know', 'Good Kid', 'Rock Alt')
musica02 = Musica('Todo Mundo Menos Você', 'Marília Mendonça', 'Sertanejo')
musica03 = Musica('My Love Mine All Mine', 'Mitski', 'Alternativo')
musica04 = Musica('Apesar de Você', 'Chico Buearque', 'MPB')
lista = [musica01, musica02, musica03, musica04]

app = Flask(__name__)
app.secret_key = 'segredo'

@app.route('/')
def listarMusicas():

    if session['usuarioLogado'] == None or 'usuarioLogado' not in session:
        return redirect('/login')
    
    return render_template('lista_musicas.html', 
                           titulo = 'Musicas Cadastradas',
                           musicas = lista)

@app.route('/cadmusicas')
def cadastrarMusica():

    if session['usuarioLogado'] == None or 'usuarioLogado' not in session:
        return redirect('/login')

    return render_template('cadastra_musica.html',
                           titulo = 'Cadastrar música')

@app.route('/addMusica', methods = ['POST',])
def adicionarMusica():
    nome = request.form['txtNomeMusica']
    banda = request.form['txtBanda']
    genero = request.form['txtGenero']

    lista.append(Musica(nome, banda, genero))

    return redirect(url_for('listarMusicas'))

@app.route('/login')
def loginUser():
    return render_template('login.html')

@app.route('/autenticar', methods = ['POST',])
def autenticar():
    if request.form['txtLogin'] in usuarios:
        
        usuario = usuarios[request.form['txtLogin']]
        
        if request.form['txtSenha'] == usuario.senha:
            session['usuarioLogado'] = request.form['txtLogin']
            flash(f"Usuário {request.form['txtLogin']} logado com sucesso!")
            return redirect(url_for('listarMusicas'))     
    else:
        flash("Usuário ou senha inválido")
        return redirect(url_for('loginUser'))

@app.route('/sair')
def sair():
    session['usuarioLogado'] = None
    return redirect(url_for('loginUser'))

app.run(debug = True)