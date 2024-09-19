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

def insertDeputado(name, party, number, laws, pec): 
    document = {
    "record": number,
    "name": name,
    "party": party,
    "laws": laws,
    "pecs": pec
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

def updateDeputadoByName(old_name, new_name, new_party):
    deputado_to_update = findDeputadoByName(old_name)
    if not deputado_to_update:
        return # Deputado não encontrado, talvez lançar uma exceção ou retornar um erro
    
    key_to_update = deputado_to_update[0]["_key"]
    document_to_update = {
        "_key": key_to_update,
        "name": new_name,
        "party": new_party
    }
    collection.update(document_to_update)

def updateDeputadoByRecord(party, number):
    deputado_to_update = findDeputadoByRecord(number)
    if not deputado_to_update:
        raise ValueError("Deputado não encontrado")

    if '_key' not in deputado_to_update[0]:
        raise KeyError("_key não encontrado em deputado_to_update")

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

def updateDeputadoPec(pecName, name):
    deputado_to_update = findDeputadoByName(name)
    key_to_update = deputado_to_update[0]["_key"]
    pec = deputado_to_update[0]["pecs"]
    document_to_update = {
        "_key": key_to_update,
        "pecs": pec + ',' + pecName
    }
    collection.update(document_to_update)

def findPecs(name):
    deputado_pecs = []
    deputado_to_take_pecs = findDeputadoByName(name)
    pecs = deputado_to_take_pecs[0]["pecs"]
    pecs = pecs.strip().split(",")
    for pec in pecs:
        pec_finded = findPecByNumber(pec)
        pec_finded = list(pec_finded)
        deputado_pecs.append(pec_finded)
    return deputado_pecs

def findPecByNumber(number):
    pec = collection_projetos.find({"pecNumber":number})
    return pec

def findAllPecs():
    cursor = db.aql.execute(
        'FOR p IN projetos_de_lei RETURN p'
    )
    pecs = list(cursor)
    return pecs



