from databasePEC import insertPEC
from databaseDeputados import findAll, updateDeputadoPec
import xmltodict
from datetime import datetime

with open("database/resultadoPesquisaPEC.xml", 'r', encoding='utf-8') as file:
    conteudo_xml = file.read()

xml_dict = xmltodict.parse(conteudo_xml)

dados = xml_dict

list_deputados = list(findAll())


for i in range(len(dados["proposicoes"]["proposicao"])):
    data_iso = dados["proposicoes"]["proposicao"][i]["dataaprensentacao"]
    data_obj = datetime.strptime(data_iso, "%Y-%m-%dT%H:%M:%SZ")
    data_formatada = data_obj.strftime("%d/%m/%Y")

    deputados = dados["proposicoes"]["proposicao"][i]["autores"].strip().split(";")

    insertPEC(dados["proposicoes"]["proposicao"][i]["title"], dados["proposicoes"]["proposicao"][i]["ementa"], dados["proposicoes"]["proposicao"][i]["autores"], data_formatada, deputados)
    
    
