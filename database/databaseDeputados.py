from arango import ArangoClient

# Criar uma instância do cliente
client = ArangoClient(hosts='http://localhost:8529')

# Conectar ao servidor ArangoDB
db = client.db('informations_Deputados_and_Projetos', username='root', password='')

# Selecionar a coleção
collection = db.collection('deputados')
collection_projetos = db.collection('projetos_de_lei')

def findAllDeputados():
    return collection.all()

def insertDeputado(name, party, number, laws): 
    document = {
    "record": number,
    "name": name,
    "party": party,
    "laws": laws,
    }
    collection.insert(document)

def deleteDeputado(name):
    deputado_to_delete = findDeputadoByName(name)
    key_to_delete = deputado_to_delete[0]["_key"]
    collection.delete(key_to_delete)

def findDeputadoByName(name):
    name = name.lower()
    name = "%" + name + "%"
    cursor = db.aql.execute(
        'FOR d IN deputados FILTER LOWER(d.name) LIKE @name RETURN d',
        bind_vars={'name': name}
    )
    deputado = list(cursor)
    return deputado

def findAll():
    names = db.aql.execute('FOR deputado IN deputados RETURN deputado.name')
    return names

def findDeputadoByRecord(number):
    cursor = db.aql.execute(
        'FOR d IN deputados FILTER d.record == @number RETURN d',
        bind_vars={'number': number}
    )
    deputado = list(cursor)
    return deputado

def updateDeputadoByName(party, name):
    deputado_to_update = findDeputadoByName(name)
    key_to_update = deputado_to_update[0]["_key"]
    document_to_update = {
        "_key": key_to_update,
        "party": party
    }
    collection.update(document_to_update)

def updateDeputadoByRecord(party, number):
    deputado_to_update = findDeputadoByRecord(number)
    key_to_update = deputado_to_update[0]["_key"]
    document_to_update = {
        "_key": key_to_update,
        "party": party
    }
    collection.update(document_to_update)

def updateDeputadoLaw(lawName, name):
    deputado_to_update = findDeputadoByName(name)
    key_to_update = deputado_to_update[0]["_key"]
    law = deputado_to_update[0]["laws"]
    document_to_update = {
        "_key": key_to_update,
        "laws": law + ',' + lawName
    }
    collection.update(document_to_update)

def findLaws(name):
    deputado_laws = []
    deputado_to_take_laws = findDeputadoByName(name)
    laws = deputado_to_take_laws[0]["laws"]
    laws = laws.strip().split(",")
    for law in laws:
        law_finded = findLawByNumber(law)
        law_finded = list(law_finded)
        deputado_laws.append(law_finded)
    return deputado_laws

def findLawByNumber(number):
    law = collection_projetos.find({"lawNumber":number})
    return law

def findAllLaws():
    cursor = db.aql.execute(
        'FOR l IN projetos_de_lei RETURN l'
    )
    laws = list(cursor)
    return laws