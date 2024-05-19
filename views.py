from flask import render_template, request, redirect, session, flash, url_for
from models import Musica, Usuario
from musica import db, app

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
