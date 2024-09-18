from databaseProjetos import insertLaw
from databaseDeputados import findAll
import xmltodict
import json

with open("database/resultadoPesquisa.xml", 'r', encoding='utf-8') as file:
    conteudo_xml = file.read()


xml_dict = xmltodict.parse(conteudo_xml)

dados = xml_dict

# Acessar o array "proposicao" corretamente
for i in range(len(dados["proposicoes"]["proposicao"])):
    pass
