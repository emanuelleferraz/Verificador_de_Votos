import requests
import json
from databaseDeputados import insertDeputado

deputados = requests.get("https://dadosabertos.camara.leg.br/api/v2/deputados?ordem=ASC&ordenarPor=nome")
deputados = deputados.json()

for i in deputados['dados']:
    insertDeputado(i['nome'], i['siglaPartido'], i['id'], "", "")
