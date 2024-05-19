from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'segredo'
app.config['SQLALCHEMY_DATABASE_URI'] = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'root',
        senha = '',
        servidor = 'localhost',
        database = 'playmusica'
    )

db = SQLAlchemy(app)

class Musica(db.Model):
    id_musica = db.Column(db.Integer, primary_key = True, autoincrement = True)
    nome_musica = db.Column(db.String(50), nullable = False)
    cantor_banda = db.Column(db.String(50), nullable = False)
    genero_musica = db.Column(db.String(20), nullable = False)

    def __repr__(self):
        return '<Name %r>' %self.name

class Usuario(db.Model):
    id_usuario = db.Column(db.Integer, primary_key = True, autoincrement = True)
    nome_usuario = db.Column(db.String(50), nullable = False)
    login_usuario = db.Column(db.String(20), nullable = False)
    senha_usuario = db.Column(db.String(15), nullable = False)

    def __repr__(self):
        return '<Name %r>' %self.name

@app.route('/')
def listarMusicas():

    if session['usuarioLogado'] == None or 'usuarioLogado' not in session:
        return redirect('/login')
    
    lista = Musica.query.order_by(Musica.id_musica)

    return render_template('lista_musicas.html', 
                           titulo = 'Musicas Cadastradas',
                           musicas = lista)

@app.route('/cadmusicas')
def cadastrarMusica():

    if session['usuarioLogado'] == None or 'usuarioLogado' not in session:
        return redirect('/login')

    return render_template('cadastra_musica.html',
                           titulo = 'Cadastrar música')

@app.route('/addMusica', methods = ['POST'])
def adicionarMusica():
    nome = request.form['txtNomeMusica']
    banda = request.form['txtBanda']
    genero = request.form['txtGenero']

    if Musica.query.filter_by(nome_musica = nome).first() and Musica.query.filter_by(cantor_banda = banda).first():
        flash("Musica ja cadastrada!", "alert alert-danger")
        return redirect(url_for('cadastrarMusica'))
    else:
        novaMusica = Musica(nome_musica = nome, cantor_banda = banda, genero_musica = genero)
        db.session.add(novaMusica)
        db.session.commit()
        flash("Musica cadastrada com sucesso", "alert alert-success")
        return redirect(url_for('cadastrarMusica'))

@app.route('/login')
def loginUser():
    return render_template('login.html')

@app.route('/autenticar', methods = ['POST'])
def autenticar():

    usuario = Usuario.query.filter_by(login_usuario = request.form['txtLogin']).first()

    if usuario:
        if request.form['txtSenha'] == usuario.senha_usuario:
            session['usuarioLogado'] = request.form['txtLogin']
            flash(f"Usuário {usuario.nome_usuario} logado com sucesso!", "alert alert-success")
            return redirect(url_for('listarMusicas'))     
        else:
            flash("Senha inválida", "alert alert-danger")
            return redirect(url_for('loginUser'))
    else:
        flash("Usuário ou senha inválido", "alert alert-danger")
        return redirect(url_for('loginUser'))

@app.route('/sair')
def sair():
    session['usuarioLogado'] = None
    return redirect(url_for('loginUser'))

app.run(debug = True)