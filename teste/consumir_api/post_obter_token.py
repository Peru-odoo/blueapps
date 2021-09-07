import requests
#from pprint import pprint

url='http://127.0.0.1:3001/tokens'
user_data = {
    "password": "12345678",
	"email": "diego@email.com",
}

response = requests.post(url=url, json=user_data)

if response.status_code >= 200 and response.status_code <= 299:
    # Sucesso
    print(response.status_code)
    print(response.reason)
#    print( response.text)
    print(response.json())
#    print('Reason', response.content)
    response_data = response.json()
    token = response_data['token']

    with open('token.txt', 'w') as file:
        file.write(token)
else:
    # Erros
    print(response.status_code)
    print(response.reason)
#    print(response.text)
    print(response.json())
#    print('Reason', response.content)