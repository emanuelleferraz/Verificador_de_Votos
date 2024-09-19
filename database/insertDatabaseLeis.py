from databaseProjetos import insertLaw
from databaseDeputados import findAll
import xmltodict
from datetime import datetime

with open("database/resultadoPesquisa.xml", 'r', encoding='utf-8') as file:
    conteudo_xml = file.read()

xml_dict = xmltodict.parse(conteudo_xml)

dados = xml_dict

list_deputados = list(findAll())
print(list_deputados)

for i in range(len(dados["proposicoes"]["proposicao"])):
    data_iso = dados["proposicoes"]["proposicao"][i]["dataaprensentacao"]
    data_obj = datetime.strptime(data_iso, "%Y-%m-%dT%H:%M:%SZ")
    data_formatada = data_obj.strftime("%d/%m/%Y")

    if dados["proposicoes"]["proposicao"][i]["autores"] in list_deputados:
        insertLaw(dados["proposicoes"]["proposicao"][i]["title"], dados["proposicoes"]["proposicao"][i]["ementa"], dados["proposicoes"]["proposicao"][i]["autores"], data_formatada)
