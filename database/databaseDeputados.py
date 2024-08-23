from arango import ArangoClient

# Criar uma instância do cliente
client = ArangoClient(hosts='http://localhost:8529')

# Conectar ao servidor ArangoDB
db = client.db('informations_Deputados_and_Projetos', username='root', password='')

# Selecionar a coleção
collection = db.collection('deputados')

def insertDeputado(name, party, number): 
    document = {
    "record": number,
    "name": name,
    "party": party,
    }
    collection.insert(document)

def deleteDeputado(name):
    deputado_to_delete = findDeputadoByName(name)
    key_to_delete = deputado_to_delete["_key"]
    collection.delete(key_to_delete)

def findDeputadoByName(name):
    deputado = collection.find({"nome":name})
    return deputado

def findDeputadoByRecord(number):
    deputado = collection.find({"record":number})
    return deputado

def updateDeputadoByName(party, name):
    deputado_to_update = findDeputadoByName(name)
    key_to_update = deputado_to_update["_key"]
    document_to_update = {
        "_key": key_to_update,
        "party": party
    }
    collection.update(document_to_update)

def updateDeputadoByRecord(party, number):
    deputado_to_update = findDeputadoByRecord(number)
    key_to_update = deputado_to_update["_key"]
    document_to_update = {
        "_key": key_to_update,
        "party": party
    }
    collection.update(document_to_update)