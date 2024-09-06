from arango import ArangoClient

# Criar uma instância do cliente
client = ArangoClient(hosts='http://localhost:8529')

# Conectar ao servidor ArangoDB
db = client.db('informations_Deputados_and_Projetos', username='root', password='')

# Selecionar a coleção
collection = db.collection('projetos')

def insertLaw(name, description, number, deputado): 
    document = {
    "lawNumber": number,
    "nome": name,
    "description": description,
    "deputado": deputado
    }
    collection.insert(document)

def deleteLaw(name):
    law_to_delete = findLawByName(name)
    key_to_delete = law_to_delete["_key"]
    collection.delete(key_to_delete)

def findLawByName(name):
    law = collection.find({"nome":name})
    return law

def findLawByNumber(number):
    law = collection.find({"lawNumber":number})
    return law

def updateLawByName(description, name):
    law_to_update = findLawByName(name)
    key_to_update = law_to_update["_key"]
    document_to_update = {
        "_key": key_to_update,
        "description": description
    }
    collection.update(document_to_update)

def updateLawByNumber(description, number):
    law_to_update = findLawByNumber(number)
    key_to_update = law_to_update["_key"]
    document_to_update = {
        "_key": key_to_update,
        "description": description
    }
    collection.update(document_to_update)