import requests
import json
import jsonpickle
import io
import pickle
try:
    to_unicode = unicode
except NameError:
    to_unicode = str

url = "http://sip.segline.srv.br/jeta/api/campanha/cliente/importado"

payload = json.dumps({
    "CAMPANHA": 6374,
    "CAMPO": "CPFCNPJ",
    "TABELA": "CAMPANHA_IMPORTACAO",
    "EMPRESA": "new",
    "JETA": 38427,
    "PAGESIZE": 2,
    "PAGEINDEX": 2
})
headers = {
    'Content-Type': 'application/json'
}


def buscar_dados_cpfcnpj(cpfcnpj):
    response = requests.request("POST", url, headers=headers, data=payload)
    dados = response.json()
    todos = json.loads(response.content)
    #    print(todos)
    print(todos['result'])


if url:
    # buscar_dados()
    buscar_dados_cpfcnpj("00001150537")

'''
# Write JSON file
with io.open('data.json', 'w', encoding='utf8') as outfile:
    str_ = json.dumps(data,
                      indent=4, sort_keys=True,
                      separators=(',', ': '), ensure_ascii=False)
    outfile.write(to_unicode(str_))



# Read JSON file
with open('data.json') as data_file:
    data_loaded = json.load(data_file)

print(data == data_loaded)
print(data_loaded)
'''

'''
with open('data.json', 'wb') as fp:
    pickle.dump(dados, fp)'''
#with open('/mnt/c/Users/Kerberos/Documents/GitHub/blueapps/teste/data.txt', 'w') as f:
#  json.dump(response, f, ensure_ascii=False)
#print(response.json())
#with open('/mnt/c/Users/Kerberos/Documents/GitHub/blueapps/teste/data.json', 'w') as f:
#    json.dump(response, f, ensure_ascii=False, indent=4)

#with open('data.txt', 'w') as f:
#  json.dump(data, f, ensure_ascii=False)

#rate = jsonpickle.encode(response)
#print(ret)
