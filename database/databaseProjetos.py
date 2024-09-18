from arango import ArangoClient
from database.databaseDeputados import updateDeputadoLaw


# Criar uma instância do cliente
client = ArangoClient(hosts='http://localhost:8529')

# Conectar ao servidor ArangoDB
db = client.db('informations_Deputados_and_Projetos', username='root', password='')

# Selecionar a coleção
collection = db.collection('projetos_de_lei')

def insertLaw(name, description, number, deputado, data): 
    document = {
    "lawNumber": number,
    "nome": name,
    "description": description,
    "deputado": deputado,
    "data": data
    }
    collection.insert(document)
    updateDeputadoLaw(number, deputado)

def deleteLaw(name):
    law_to_delete = findLawByName(name)
    key_to_delete = law_to_delete[0]["_key"]
    collection.delete(key_to_delete)

def findLawByName(name):
    cursor = db.aql.execute(
        'FOR l IN projetos_de_lei FILTER l.nome == @name RETURN l',
        bind_vars={'name': name}
    )
    law = list(cursor)
    return law

def findLawByNumber(number):
    cursor = db.aql.execute(
        'FOR l IN projetos_de_lei FILTER l.lawNumber == @number RETURN l',
        bind_vars={'number': number}
    )
    law = list(cursor)
    return law

def updateLawByName(description, name):
    law_to_update = findLawByName(name)
    key_to_update = law_to_update[0]["_key"]
    document_to_update = {
        "_key": key_to_update,
        "description": description
    }
    collection.update(document_to_update)

def updateLawByNumber(description, number):
    law_to_update = findLawByNumber(number)
    key_to_update = law_to_update[0]["_key"]
    document_to_update = {
        "_key": key_to_update,
        "description": description
    }
    collection.update(document_to_update)

def findAllLaws():
    cursor = db.aql.execute(
        'FOR l IN projetos_de_lei RETURN l'
    )
    laws = list(cursor)
    return laws