import sys, os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'database')))
from flask import Flask, render_template, session, flash, request, redirect, url_for, jsonify
from database.databaseDeputados import findAllDeputados, deleteDeputado, updateDeputadoByName, findDeputadoByName, insertDeputado
from database.databaseProjetos import findAllLaws, findLawsByDeputadoName, deleteLaw, updateLawByName, insertLaw, findLawByName
from database.databasePEC import findAllPECs, findPECsByDeputadoName
from database.databaseAdministrador import buscar_usuario
                 
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


@app.route("/pecs")
def pecs():
    pec_list = findAllPECs()
    return render_template("pecs.html", pecs=pec_list)

@app.route("/deputados_pecs")
def deputados_pecs():
    deputado_name = request.args.get('deputado')
    pecs_do_deputado = findPECsByDeputadoName(deputado_name)

    return render_template("deputadosPecs.html", pecs=pecs_do_deputado, deputado=deputado_name)

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

@app.route('/add_deputado', methods=['POST'])
def add_deputado():
    data = request.get_json()
    name = data.get('name')
    party = data.get('party')
    record = data.get('record')

    # Verificar se o deputado já existe
    deputado_exists = findDeputadoByName(name)
    if deputado_exists:
        return jsonify({'message': 'Deputado já cadastrado'}), 400
    
    # Inserir o novo deputado
    insertDeputado(name, party, record, "", "")
    return jsonify({'message': 'Deputado adicionado com sucesso!'}), 200

@app.route('/edit_deputado', methods=['POST'])
def edit_deputado():
    data = request.get_json()
    old_name = data.get('old_name')
    new_name = data.get('new_name')
    new_party = data.get('party')

    if new_name != old_name:  
        deputado_existente = findDeputadoByName(new_name)
        if deputado_existente:
            return jsonify({'message': 'Deputado já cadastrado'}), 400

    
    updateDeputadoByName(old_name, new_name, new_party)
    return jsonify({'message': 'Deputado atualizado com sucesso!'}), 200

# Excluir Deputado
@app.route('/delete_deputado', methods=['POST'])
def delete_deputado():
    data = request.get_json()
    name = data.get('name')
    
    
    deleteDeputado(name)
    return jsonify({'message': 'Deputado excluído com sucesso!'}), 200


if __name__ in "__main__":
    app.run(debug=True, port=20000)