import sys, os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'database')))
from flask import Flask, render_template, session, flash, request, redirect, url_for, jsonify
from database.databaseDeputados import findAllDeputados, deleteDeputado, updateDeputadoByName, findDeputadoByName, insertDeputado
from database.databaseProjetos import findAllLaws, findLawsByDeputadoName, deleteLaw, updateLawByName, insertLaw, findLawByName
from database.databasePEC import findAllPECs, findPECsByDeputadoName, updatePEC
from database.databaseAdministrador import buscar_usuario
from database.databasePEC import findPECByName, insertPEC, updatePECByName, updateDeputadoPec, deletePEC
from datetime import date, datetime
                 
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

    return render_template("projetoLeis.html", leis=leis_list, current_date=date.today().isoformat())


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


@app.route('/add_lei', methods=['POST'])
def add_lei():
    data = request.json
    name = data.get('name')
    description = data.get('description')
    deputado = data.get('deputado')
    data_apresentacao = data.get('data')

    # Verificar se já existe uma lei com o mesmo nome
    if findLawByName(name):
        return jsonify({'error': 'Já existe uma lei com esse nome.'}), 400

    # Verificar se o deputado existe
    if not findDeputadoByName(deputado):
        return jsonify({'error': 'Deputado não encontrado.'}), 400

    # Verificar se a data é válida
    try:
        # Tente converter a data para o formato desejado
        datetime.strptime(data_apresentacao, '%Y-%m-%d')  # Ajuste o formato conforme necessário
    except ValueError:
        return jsonify({'error': 'Data inválida. Utilize o formato YYYY-MM-DD.'}), 400

    # Chame a função para inserir a lei
    insertLaw(name, description, deputado, data_apresentacao)
    return jsonify({'message': 'Lei adicionada com sucesso!'}), 201


@app.route('/delete_lei', methods=['POST'])
def delete_lei():
    data = request.get_json()
    law_name = data.get('name')
    
    try:
        deleteLaw(law_name)  # Chama a função para excluir a lei
        return jsonify({"message": "Lei excluída com sucesso!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/edit_lei', methods=['POST'])
def edit_lei():
    data = request.json
    old_name = data.get('name')  # Nome atual
    new_name = data.get('new_name')  # Novo nome (você precisa enviar isso)
    description = data.get('description')
    data_apresentacao = data.get('data')


    print(data)
    # Chame a função para atualizar a lei
    updated_law = updateLawByName(new_name, description, data_apresentacao, old_name)

    if updated_law:
        return jsonify({'message': 'Lei editada com sucesso!'}), 200
    else:
        return jsonify({'error': 'Lei não encontrada!'}), 404
    
@app.route('/add_pec', methods=['POST'])
def add_pec():
    name = request.form.get('name')
    description = request.form.get('description')
    deputados = request.form.get('deputado')
    data_apresentacao = request.form.get('data')

    # Lógica para verificar se a PEC já existe e inseri-la no banco
    pec_existente = findPECByName(name)
    if pec_existente:
        return jsonify({'error': 'PEC já cadastrada'}), 400

    # Verificar se o campo de deputados não está vazio
    if not deputados:
        return jsonify({'error': 'Por favor, insira pelo menos um deputado.'}), 400

    # Dividir os deputados por vírgula e remover espaços
    array_deputados = [deputado.strip() for deputado in deputados.split(',')]

    # Verificar se todos os deputados existem
    for deputado in array_deputados:
        if not findDeputadoByName(deputado):
            return jsonify({'error': f'Deputado "{deputado}" não encontrado.'}), 400

    # Converter a data para o formato brasileiro (DD/MM/AAAA)
    try:
        data_formatada = datetime.strptime(data_apresentacao, '%Y-%m-%d').strftime('%d/%m/%Y')
    except ValueError:
        return jsonify({'error': 'Formato de data inválido. Use AAAA-MM-DD.'}), 400

    # Inserir a nova PEC
    insertPEC(name, description, data_formatada, array_deputados)
    
    return jsonify({'message': 'PEC adicionada com sucesso!'}), 200

@app.route('/edit_pec', methods=['POST'])
def edit_pec():
    data = request.get_json()
    old_name = data.get('old_name')
    new_name = data.get('new_name')
    new_description = data.get('description')
    new_data = data.get('data') 

    print(data)

    # Verificar se a nova PEC já existe
    if new_name and new_name != old_name:  
        pec_existente = findPECByName(new_name)
        if pec_existente:
            return jsonify({'message': 'PEC já cadastrada'}), 400

    # Formatar a data no formato dd/mm/yyyy
    if new_data:
        # Converter a data de yyyy-mm-dd para dd/mm/yyyy
        year, month, day = new_data.split("-")
        new_data = f"{day}/{month}/{year}"

    # Atualizar a PEC
    try:
        updatePEC(old_name, new_name, new_description, new_data)
    except ValueError as e:
        return jsonify({'message': str(e)}), 400  # Retorna erro se a PEC não for encontrada

    return jsonify({'message': 'PEC atualizada com sucesso!'}), 200

# Excluir PEC
@app.route('/delete_pec', methods=['POST'])
def delete_pec():
    data = request.get_json()
    name = data.get('name')

    deletePEC(name)
    return jsonify({'message': 'PEC excluída com sucesso!'}), 200


if __name__ in "__main__":
    app.run(debug=True, port=20000)