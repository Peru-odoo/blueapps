import requests
import json

#6374
campanha = input("Digite o Código da Campanha: ")

if len(campanha) != 4:
    print("Quantidade de dígitos invalido")
    exit()

quantidade = input("Quantidade de Leads: ")

url = "http://sip.segline.srv.br/jeta/api/campanha/cliente/importado"
payload = json.dumps({
  "CAMPANHA": (campanha),
  "CAMPO": "CPFCNPJ",
  "TABELA": "CAMPANHA_IMPORTACAO",
  "EMPRESA": "new",
  "JETA": 38427,
  "PAGESIZE": (quantidade),
  "PAGEINDEX": 2
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
#print('Campanha: {}'.format(response['code']))



