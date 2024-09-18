from flask import Flask, render_template, session, flash, request, redirect, url_for
from database.databaseDeputados import findAllDeputados
from database.databaseAdministrador import buscar_usuario
from database.databaseProjetos import findAllLaws

#Inicialização
app = Flask(__name__)
app.secret_key = "minha_chave"

#Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/deputados")
def deputados():
    deputados_list = findAllDeputados()
    return render_template("deputados.html", deputados=deputados_list)

@app.route("/projeto_leis")
def projeto_leis():
    leis_list = findAllLaws()

    return render_template("projetoLeis.html", leis=leis_list)

@app.route("/conexoes")
def conexoes():
    return render_template("conexoes.html")
    
@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def loginPost():

    user = request.form['user']
    password = request.form['password']

    # Chamar a função para buscar o usuário
    usuario = buscar_usuario(user, password)

    if usuario:
        # Usuário encontrado, armazenar as informações na sessão
        session['user'] = usuario['user']
        session['user_id'] = usuario['_key']

        return redirect(url_for('index'))
    
    else:
        flash('Usuário ou senha incorretos')
        return render_template("login.html") 
    
@app.route("/logout")
def logout():

    session.pop('user', None)
    session.pop('user_id', None)
    return redirect(url_for('index'))   

if __name__ in "__main__":
    app.run(debug=True, port=20000)