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
    return render_template("deputadoteste.html", deputados=deputados_list)

@app.route("/login")
def login():
    return render_template("login.html")

if __name__ in "__main__":
    app.run(debug=True, port=20000)


