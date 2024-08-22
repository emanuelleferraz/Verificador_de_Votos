from arango import ArangoClient

# Criando um cliente para ArangoDB
client = ArangoClient(hosts='http://localhost:8529')

# Conectando ao banco de dados _system com o usuário root
sys_db = client.db('_system', username='root', password='')

# Criar um novo banco de dados se não existir
if not sys_db.has_database('informations_Deputados_and_Projetos'):
    sys_db.create_database('informations_Deputados_and_Projetos')

# Agora conectando ao novo banco de dados
db = client.db('informations_Deputados_and_Projetos', username='root', password='')

# Criar uma nova coleção deputados se não existir
if not db.has_collection('deputados'):
    db.create_collection('deputados')

# Criar uma nova coleção projetos de lei se não existir
if not db.has_collection('projetos_de_lei'):
    db.create_collection('projetos_de_lei')

