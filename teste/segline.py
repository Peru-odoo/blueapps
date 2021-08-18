import requests
print("################")
print("# Consulta Segline #")
print("################")
print()


request = requests.get('http://sip.segline.srv.br/jeta/api/campanha?EMPRESA=new&CAMPO=DESCRICAO&SITUACAO=1&PAGEINDEX=1&ABERTO=S&AGENTE=J9641997&jeta=38427')
campanhas = request.json()

if 'erro' not in campanhas:
    print('Código: {}'.format(campanhas['codigo']))
    print('Descrição: {}'.format(campanhas['codigoDescricao']))
    print('Campanha: {}'.format(campanhas['descricao']))
    print('Situação: {}'.format(campanhas['situacao']))
    print('Data de Inicio: {}'.format(campanhas['dataInicio']))
    print('Data Final: {}'.format(campanhas['dataFim']))
    print('Observação: {}'.format(campanhas['obs']))
    print('Quantidade: {}'.format(campanhas['qtdedisponivel']))


