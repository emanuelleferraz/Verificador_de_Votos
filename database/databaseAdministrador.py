from arango import ArangoClient

# Criar uma instância do cliente
client = ArangoClient(hosts='http://localhost:8529')

# Conectar ao servidor ArangoDB
db = client.db('informations_Deputados_and_Projetos', username='root', password='')

# Selecionar a coleção
collection = db.collection('administrador')

def buscar_usuario(user, senha):

    query = '''
    FOR doc IN administrador
        FILTER doc.user == @user AND doc.senha == @senha
        RETURN doc
    '''

    bind_vars = {
        'user': user,
        'senha': senha
    }

    cursor = db.aql.execute(query, bind_vars=bind_vars)
    result = [doc for doc in cursor]

    if result:
        return result[0] 
    else:
        return None  
