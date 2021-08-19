from typing import MutableMapping
import requests
from pprint import pprint

from requests.api import head
from get_token import token

mimetypes = MimeTypes()
arquivo = 'pp.jpg'
mimetype_arquivo=mimetypes.guess_type(arquivo)[0]

multipart = MultipartEncoder(fields={
    'aluno_id': '2',
    'foto': (arquivo, open(arquivo, 'rb'), mimetype_arquivo)
})

url='http://127.0.0.1:3001/fotos'

headers = {
    'Authorization' : token,
    'Content-Type' : multipart.content_type
}
user_data = {
#	"nome": "Jessika",
#	"sobrenome": "Franco"
#	"email": "email3@email3.com",
#	"idade": "24",
#	"peso": "81.04",
#	"altura": "1.90"
}

response = requests.post(url=url, json=user_data, headers=headers)

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