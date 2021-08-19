#!/usr/bin/python3
import os, sys, requests
import json
print("################")
print("# Consulta Segline #")
print("################")
print()

request = requests.get('http://sip.segline.srv.br/jeta/api/campanha?EMPRESA=new&CAMPO=DESCRICAO&SITUACAO=1&PAGEINDEX=1&ABERTO=S&AGENTE=J9641997&jeta=38427')
campanhas = request.json()

dados = campanhas
parsed_json = json.loads(dados)
if 'erro' not in campanhas:
     print(campanhas)
#    print('Descri??o: {}'.format(campanhas['codigoDescricao']))
#    print('Campanha: {}'.format(campanhas['descricao']))
#    print('Situa??o: {}'.format(campanhas['situacao']))
#    print('Data de Inicio: {}'.format(campanhas['dataInicio']))
#    print('Data Final: {}'.format(campanhas['dataFim']))
#    print('Observa??o: {}'.format(campanhas['obs']))
#    print('Quantidade: {}'.format(campanhas['qtdedisponivel']))


