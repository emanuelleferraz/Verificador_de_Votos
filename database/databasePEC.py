from arango import ArangoClient
from databaseDeputados import updateDeputadoPec, findAll

# Criar uma instância do cliente
client = ArangoClient(hosts='http://localhost:8529')

# Conectar ao servidor ArangoDB
db = client.db('informations_Deputados_and_Projetos', username='root', password='')

# Selecionar a coleção
collection = db.collection('pec')

def insertPEC(name, description, data, array_deputados): 
    document = {
    "name": name,
    "description": description,
    "deputado": '; '.join(array_deputados),
    "data": data
    }
    collection.insert(document)

    list_deputados = list(findAll())

    for dep in array_deputados:
        if dep in list_deputados:
            updateDeputadoPec(name, dep) 

def deletePEC(name):
    PEC_to_delete = findPECByName(name)
    key_to_delete = PEC_to_delete[0]["_key"]
    collection.delete(key_to_delete)

def findPECByName(name):
    cursor = db.aql.execute(
        'FOR p IN pec FILTER p.name == @name RETURN p',
        bind_vars={'name': name}
    )
    pec = list(cursor)
    return pec

def updatePECByName(description, name):
    PEC_to_update = findPECByName(name)

    # Verifica se a PEC foi encontrada
    if not PEC_to_update:
        raise ValueError("PEC não encontrada.")  # ou retornar um erro apropriado

    key_to_update = PEC_to_update[0]["_key"]
    document_to_update = {
        "_key": key_to_update,
        "description": description
    }
    collection.update(document_to_update)
def findAllPECs():
    cursor = db.aql.execute(
        'FOR l IN pec RETURN l'
    )
    PECs = list(cursor)

    pecs_list = []
    for pec in PECs:
        deps = pec["deputado"].strip().split(";")
        if len(deps) > 5:
            pec["deputado"] = deps[0] + ", " + deps[1] + ", " + deps[2] + ", " + deps[3] + ", " + deps[4] + " - e outros"
        else:
             pec["deputado"] = pec["deputado"].replace(";", ", ")

        pecs_list.append(pec)

    return pecs_list

def findPECsByDeputadoName(deputado_name):
    deputado_name = deputado_name.lower()
    deputado_name = "%" + deputado_name + "%"
    cursor = db.aql.execute(
        'FOR p IN pec FILTER LOWER(p.deputado) LIKE @deputado RETURN p',
        bind_vars={'deputado': deputado_name}
    )
    PECs = list(cursor)
    return PECs

def updatePEC(old_name, new_name, new_description, new_data):
    # Verificar se a PEC existe
    pec_to_update = findPECByName(old_name)
    if not pec_to_update:
        raise ValueError("PEC não encontrada.")

    # Preparar o documento para atualização
    key_to_update = pec_to_update[0]["_key"]
    document_to_update = {
        "_key": key_to_update,
        "name": new_name if new_name else old_name,  # Mantém o nome antigo se não houver novo
        "description": new_description if new_description else pec_to_update[0]["description"],  # Mantém a descrição antiga se não houver nova
        "data": new_data if new_data else pec_to_update[0]["data"]  # Mantém a data antiga se não houver nova
    }

    # Atualiza a PEC na coleção
    collection.update(document_to_update)

    # Se o nome foi alterado, atualize os deputados relacionados
    if new_name and new_name != old_name:
        list_deputados = list(findAll())
        for dep in pec_to_update[0]["deputado"].strip().split("; "):
            if dep in list_deputados:
                updateDeputadoPec(new_name, dep)  # Atualiza o deputado com o novo nome da PEC
