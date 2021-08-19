import requests
from pprint import pprint
from requests.api import head
from get_token import token

url='http://127.0.0.1:3001/alunos/2'

headers = {
#    'Authorization' : token
}
user_data = {
#	"nome": "Jessika",
#	"sobrenome": "Oliveira"
#	"email": "email2@email2.com",
#	"idade": "55",
#	"peso": "81.04",
#	"altura": "1.90"
}

response = requests.delete(url=url, json=user_data, headers=headers)

if response.status_code >= 200 and response.status_code <= 299:
    # Sucesso
    print(response.status_code)
    print(response.reason)
    print(response.json())
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