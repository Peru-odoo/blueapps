import requests
from pprint import pprint

from requests.api import head
from get_token import token

url='http://127.0.0.1:3001/alunos'

headers = {
#    'Authorization' : token
}
user_data = {
#	"nome": "Paulo",
#	"sobrenome": "Silva",
#	"email": "email2@email2.com",
#	"idade": "55",
#	"peso": "81.04",
#	"altura": "1.90"
}

response = requests.get(url=url, json=user_data, headers=headers)

if response.status_code >= 200 and response.status_code <= 299:
    # Sucesso
    response_data = response.json()
    print(response.status_code)
    print(response.reason)
# Imprimir apenas o nome, caso retorne apenas um registro
#    print(response_data['nome'])
    for aluno in response_data: #Pegar apenas o nome e email de cada registro que retornar
        print(aluno['nome','email'])
#        print(aluno['email'])
#    print(response.json())

#    print( response.text)
#    print('Reason', response.content)
#    response_data = response.json()
#    token = response_data['token']

#    with open('token.txt', 'w') as file:
#        file.write(token)
else:
    # Erros
    print(response.status_code)
    print(response.reason)
    print(response.json())
#    print(response.text)
#    print('Reason', response.content)