import json
import jsonpickle
import requests

#6374
#campanha = input("Digite o Código da Campanha: ")
campanha = 6374
#if len(campanha) != 4:
#    print("Quantidade de dígitos invalido")
#    exit()

#quantidade = input("Quantidade de Leads: ")

url = "http://sip.segline.srv.br/jeta/api/campanha/cliente/importado"
payload = json.dumps({
  "CAMPANHA": (campanha),
  "CAMPO": "CPFCNPJ",
  "TABELA": "CAMPANHA_IMPORTACAO",
  "EMPRESA": "new",
  "JETA": 38427,
  "PAGESIZE": 1,
  "PAGEINDEX": 2
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

dados = response
dados1 = json.dumps(dados)
dados2 = jsonpickle.encode(dados)
parsed_json = json.loads(dados)
#print(response.text)
#print(dados2)



