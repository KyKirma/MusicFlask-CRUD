from flask import render_template, request, redirect, session, flash, url_for
from musica import app, db
from definicoes import FormularioUsuario, FormularioCadastro
from flask_bcrypt import generate_password_hash, check_password_hash

@app.route('/login')
def loginUser():
    form = FormularioUsuario()
    return render_template('login.html',
                           form = form,
                           titulo = 'Logar')

@app.route('/autenticar', methods = ['POST'])
def autenticar():
    from models import Usuario
    form = FormularioUsuario(request.form)

    usuario = Usuario.query.filter_by(login_usuario = form.usuario.data).first()
    senha = check_password_hash(usuario.senha_usuario, form.senha.data)

    if usuario and senha:
        session['usuarioLogado'] = usuario.login_usuario
        flash(f"Usuário {usuario.nome_usuario} logado com sucesso!", "alert alert-success")
        return redirect(url_for('listarMusicas'))

    flash("Usuário ou senha inválido", "alert alert-danger")
    return redirect(url_for('loginUser'))
    
@app.route('/cadastrar')
def cadastrarUsuario():
    form = FormularioCadastro()

    return render_template('cadastra_usuario.html',
                           titulo = 'Cadastrar Usuário',
                           form = form)

@app.route('/addUsuario', methods = ['POST'])
def adicionarUsuario():
    formRecebido = FormularioCadastro(request.form)

    if not formRecebido.validate_on_submit():
        return redirect(url_for('cadastrarUsuario'))
    
    nome = formRecebido.nome.data
    usuario = formRecebido.usuario.data
    senha = generate_password_hash(formRecebido.senha.data).decode('utf-8')

    from models import Usuario
    usuario_existe = Usuario.query.filter_by(login_usuario = usuario).first()

    if usuario_existe:
        flash('Usuario já cadastrado!', "alert alert-danger")
        return redirect(url_for('cadastrarUsuario'))
    
    novo_usuario = Usuario(nome_usuario = nome, login_usuario = usuario, senha_usuario = senha)
    db.session.add(novo_usuario)
    db.session.commit()

    flash(f"Usuário cadastrado com sucesso!", "alert alert-success")
    return redirect(url_for('loginUser'))