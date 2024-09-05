from flask import Flask, render_template
from database.databaseDeputados import findAllDeputados

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
    return render_template("projetoLeis.html")

@app.route("/conexoes")
def conexoes():
    return render_template("conexoes.html")
    
@app.route("/login")
def login():
    return render_template("login.html")

if __name__ in "__main__":
    app.run(debug=True, port=20000)