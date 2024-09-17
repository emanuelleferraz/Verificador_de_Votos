import databaseDeputados as db
from databaseProjetos import findLawByNumber

#print(db.findDeputadoByName('ANA'))

#print(db.findDeputadoByRecord(107970))

#db.insertDeputado('teste', 'teste', 10)

#db.deleteDeputado('teste')

#print(db.findDeputadoByRecord(10))

#law = findLawByNumber("11000")

print(db.findLaws("Acácio Favacho"))
