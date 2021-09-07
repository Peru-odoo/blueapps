import requests
print("################")
print("# Consulta CEP #")
print("################")
print()

cep_imput = input("Digite o CEP para a Consulta: ")
if len(cep_imput) != 8:
    print("Quantidade de dígitos invalido")
    exit()
request = requests.get('https://viacep.com.br/ws/{}/json/'.format(cep_imput))
address_data = request.json()

if 'erro' not in address_data:
    print('==> CEP ENCONTRADO <==')
    print('CEP: {}'.format(address_data['cep']))
    print('Rua: {}'.format(address_data['logradouro']))
    print('Complemento: {}'.format(address_data['complemento']))
    print('Estado: {}'.format(address_data['uf']))
    print('DDD: {}'.format(address_data['ddd']))
    #print(request.json())
else:
    print('CEP Invalido.'.format(cep_imput))

option = int(input('Deseja realizar uma nova consulta? \n 1. Sim\n 2. Não\n'))
if option == 1:
    main.py
else:
    print('Saindo..')
#print(request.json())

