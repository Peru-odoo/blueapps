import requests
#from pprint import pprint

url='http://127.0.0.1:3001/users'
user_data = {
	"nome": "Diego",
    "password": "12345678",
	"email": "diego@email.com",
}

response = requests.post(url=url, json=user_data)

if response.status_code >= 200 and response.status_code <= 299:
    # Sucesso
    print(response.status_code)
    print(response.reason)
    print( response.text)
    print(response.json())
#    print('Reason', response.content)
else:
    # Erros
    print(response.status_code)
    print(response.reason)
    print(response.text)
    print(response.json())
#    print('Reason', response.content)