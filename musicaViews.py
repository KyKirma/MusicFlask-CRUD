from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from models import Musica
from musica import db, app
from definicoes import recupera_imagem, deletar_imagem, FormularioMusica
import time

@app.route('/')
def listarMusicas():
    if 'usuarioLogado' not in session or session['usuarioLogado'] == None:
        return redirect(url_for('loginUser'))
    
    lista = Musica.query.order_by(Musica.id_musica)

    return render_template('lista_musicas.html', 
                           titulo = 'Musicas Cadastradas',
                           musicas = lista)


@app.route('/cadmusicas')
def cadastrarMusica():

    if session['usuarioLogado'] == None or 'usuarioLogado' not in session:
        return redirect(url_for('loginUser'))

    form = FormularioMusica()

    return render_template('cadastra_musica.html',
                           titulo = 'Cadastrar música',
                           form = form)


@app.route('/addMusica', methods = ['POST'])
def adicionarMusica():

    formRecebido = FormularioMusica(request.form)

    if not formRecebido.validate_on_submit():
        return redirect(url_for('cadastrar_musica'))
    
    nome = formRecebido.nome.data
    banda = formRecebido.grupo.data
    genero = formRecebido.genero.data

    if Musica.query.filter_by(nome_musica = nome).first() and Musica.query.filter_by(cantor_banda = banda).first():
        flash("Musica ja cadastrada!", "alert alert-danger")
        return redirect(url_for('cadastrarMusica'))
    else:
        novaMusica = Musica(nome_musica = nome, cantor_banda = banda, genero_musica = genero)
        db.session.add(novaMusica)
        db.session.commit()

        arquivo = request.files['arquivo']

        if arquivo:
            pastaArquivo = app.config['UPLOAD_PASTA']
            arquivoNome = arquivo.filename
            arquivoNome = arquivoNome.split('.')
            extensao = arquivoNome[len(arquivoNome) - 1]
            momento = time.time()

            nome_completo = f'album{novaMusica.id_musica}_{momento}.{extensao}'
            
            arquivo.save(f'{pastaArquivo}/{nome_completo}')

        flash("Musica cadastrada com sucesso", "alert alert-success")
        return redirect(url_for('cadastrarMusica'))


@app.route('/editar/<int:id>')
def editar(id):

    if session['usuarioLogado'] == None or 'usuarioLogado' not in session:
        return redirect(url_for('loginUser'))

    musicaBuscada = Musica.query.filter_by(id_musica = id).first()

    form = FormularioMusica()
    form.nome.data = musicaBuscada.nome_musica
    form.grupo.data = musicaBuscada.cantor_banda
    form.genero.data = musicaBuscada.genero_musica

    album = recupera_imagem(id)

    return render_template('editar_musica.html',
                           titulo = 'Editar música',
                           musica = form,
                           albumMusica = album,
                           id = id)


@app.route('/attMusica', methods = ['POST'])
def atualizarMusica():
    formRecebido = FormularioMusica(request.form)
    
    if formRecebido.validate_on_submit():
        musica = Musica.query.filter_by(id_musica = request.form['txtId']).first()

        musica.nome_musica = formRecebido.nome.data
        musica.cantor_banda = formRecebido.grupo.data
        musica.genero_musica = formRecebido.genero.data

        db.session.add(musica)
        db.session.commit()

        arquivo = request.files['arquivo']
        
        if arquivo:
            pastaArquivo = app.config['UPLOAD_PASTA']
            arquivoNome = arquivo.filename
            arquivoNome = arquivoNome.split('.')
            extensao = arquivoNome[len(arquivoNome) - 1]
            momento = time.time()

            nome_completo = f'album{musica.id_musica}_{momento}.{extensao}'

            deletar_imagem(musica.id_musica)

            arquivo.save(f'{pastaArquivo}/{nome_completo}')

        flash('Musica Editada com sucesso', "alert alert-success")
        return redirect(url_for('listarMusicas'))
    flash('Ocorreu algum erro.', "alert alert-danger")
    return redirect(url_for('listarMusicas'))

@app.route('/excluir/<int:id>')
def excluir(id):

    if 'usuarioLogado' not in session or session['usuarioLogado'] == None:
        return redirect(url_for('loginUser'))
    
    Musica.query.filter_by(id_musica = id).delete()
    deletar_imagem(id)
    db.session.commit()

    flash("Musica excluida com sucesso", "alert alert-success")
    return redirect(url_for('listarMusicas'))

@app.route('/uploads/<nomeImagem>')
def imagem(nomeImagem):
    return send_from_directory('uploads', nomeImagem)

@app.route('/sair')
def sair():
    session['usuarioLogado'] = None
    return redirect(url_for('loginUser'))
