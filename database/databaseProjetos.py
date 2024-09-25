from arango import ArangoClient
from databaseDeputados import updateDeputadoLaw


# Criar uma instância do cliente
client = ArangoClient(hosts='http://localhost:8529')

# Conectar ao servidor ArangoDB
db = client.db('informations_Deputados_and_Projetos', username='root', password='')

# Selecionar a coleção
collection = db.collection('projetos_de_lei')

def insertLaw(name, description, deputado, data): 
    document = {
    "name": name,
    "description": description,
    "deputado": deputado,
    "data": data
    }
    collection.insert(document)
    updateDeputadoLaw(name, deputado)

def deleteLaw(name):
    law_to_delete = findLawByName(name)
    key_to_delete = law_to_delete[0]["_key"]
    collection.delete(key_to_delete)

def findLawByName(name):
    cursor = db.aql.execute(
        'FOR l IN projetos_de_lei FILTER l.name == @name RETURN l',
        bind_vars={'name': name}
    )
    law = list(cursor)
    return law

def updateLawByName(new_name, new_description, new_data_apresentacao, old_name):
    # Encontrar a lei pelo nome atual
    law_to_update = findLawByName(old_name)
    
    if not law_to_update:
        return None  # Lei não encontrada
    
    # Pegar a chave do documento
    key_to_update = law_to_update[0]["_key"]
    
    # Criar o novo documento com os dados atualizados (sem alterar o deputado)
    document_to_update = {
        "_key": key_to_update,
        "name": new_name,
        "description": new_description,
        "data": new_data_apresentacao
    }
    
    # Atualizar o documento no banco de dados
    collection.update(document_to_update)
    return document_to_update

def findAllLaws():
    cursor = db.aql.execute(
        'FOR l IN projetos_de_lei RETURN l'
    )
    laws = list(cursor)
    return laws

def findLawsByDeputadoName(deputado_name):
    cursor = db.aql.execute(
        'FOR l IN projetos_de_lei FILTER l.deputado == @deputado RETURN l',
        bind_vars={'deputado': deputado_name}
    )
    laws = list(cursor)
    return laws