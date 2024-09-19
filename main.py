import sys, os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'database')))
from flask import Flask, render_template, session, flash, request, redirect, url_for
from database.databaseDeputados import findAllDeputados
from database.databaseDeputados import insertDeputado
from database.databaseDeputados import findDeputadoByName
from database.databaseDeputados import updateDeputadoByName
from database.databaseDeputados import deleteDeputado
from database.databaseAdministrador import buscar_usuario
from database.databaseProjetos import findAllLaws
from database.databaseProjetos import findLawByName
from database.databaseProjetos import insertLaw
from database.databaseProjetos import updateLawByName
from database.databaseProjetos import deleteLaw
from database.databaseProjetos import findLawsByDeputadoName
                                       
#Inicialização
app = Flask(__name__)
app.secret_key = "minha_chave"

#Routes
@app.route("/")
def index():
    user_id = session.get('user_id')
    return render_template("index.html", user_id=user_id)

@app.route("/deputados")
def deputados():
    deputados_list = findAllDeputados()
    return render_template("deputados.html", deputados=deputados_list)

@app.route("/projeto_leis")
def projeto_leis():
    leis_list = findAllLaws()

    return render_template("projetoLeis.html", leis=leis_list)

@app.route("/deputados_leis")
def deputados_leis():

    deputado_name = request.args.get('deputado')
    leis_do_deputado = findLawsByDeputadoName(deputado_name)

    return render_template("deputadosLeis.html", leis=leis_do_deputado, deputado=deputado_name)


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

@app.route("/adm")
def adm():
    # Busca dados de deputados e leis para exibir na página de administração
    deputados_list = findAllDeputados()
    leis_list = findAllLaws()
    
    # Renderiza a página de administração passando os dados
    return render_template("administracao.html", deputados=deputados_list, leis=leis_list)


    

if __name__ in "__main__":
    app.run(debug=True, port=20000)